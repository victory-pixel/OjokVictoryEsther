import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from snake_game import SnakeGameAI, Direction, Point

# ─── Hyperparameters ───────────────────────────────────────────
MAX_MEMORY   = 100_000  # how many past experiences to remember
BATCH_SIZE   = 1000     # how many experiences to learn from at once
LEARNING_RATE = 0.001   # how fast the model updates its weights

# ─── Neural Network ────────────────────────────────────────────
class LinearQNet(nn.Module):
    """
    A simple 3-layer neural network:
    Input layer → Hidden layer → Output layer
    Input:  11 values describing the game state
    Output: 3 values (scores for straight, right, left)
    """
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # input → hidden
        self.fc2 = nn.Linear(hidden_size, output_size) # hidden → output

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU activation on hidden layer
        x = self.fc2(x)              # raw scores for each action
        return x

    def save(self, filename='model.pth'):
        """Save the trained model so we don't lose progress."""
        torch.save(self.state_dict(), filename)
        print(f"Model saved as {filename}")


# ─── Q-Learning Trainer ────────────────────────────────────────
class QTrainer:
    """
    Handles the actual learning using the Bellman equation:
    Q_new = reward + gamma * max(Q(next_state))
    Basically: the value of an action = immediate reward + future reward potential
    """
    def __init__(self, model, lr, gamma):
        self.model   = model
        self.gamma   = gamma        # discount rate for future rewards (0-1)
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()  # Mean Squared Error loss

    def train_step(self, state, action, reward, next_state, done):
        # Convert everything to tensors (what PyTorch works with)
        state      = torch.tensor(np.array(state),      dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action     = torch.tensor(np.array(action),     dtype=torch.long)
        reward     = torch.tensor(np.array(reward),     dtype=torch.float)

        # If a single experience (not a batch), add a dimension
        if len(state.shape) == 1:
            state      = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action     = torch.unsqueeze(action, 0)
            reward     = torch.unsqueeze(reward, 0)
            done       = (done, )

        # 1. Predict Q values for current state
        pred = self.model(state)
        target = pred.clone()

        # 2. Update Q value using Bellman equation
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 3. Backpropagation — update the network weights
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()


# ─── The Agent ─────────────────────────────────────────────────
class Agent:
    """
    The RL agent that:
    - Observes the game state
    - Decides what action to take
    - Remembers past experiences
    - Learns from those experiences
    """
    def __init__(self):
        self.n_games  = 0       # number of games played so far
        self.epsilon  = 0       # controls exploration vs exploitation
        self.gamma    = 0.9     # discount rate (how much future rewards matter)
        self.memory   = deque(maxlen=MAX_MEMORY)  # stores past experiences

        # Create the neural network and trainer
        self.model   = LinearQNet(11, 256, 3)  # 11 inputs, 256 hidden, 3 outputs
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        """
        Build an 11-value snapshot of the current game state.
        This is what the agent 'sees' before making a decision.
        """
        head = game.snake[0]
        block = 20  # BLOCK_SIZE

        # Points one step ahead in each direction from the head
        pt_l = Point(head.x - block, head.y)
        pt_r = Point(head.x + block, head.y)
        pt_u = Point(head.x, head.y - block)
        pt_d = Point(head.x, head.y + block)

        # Current direction (one-hot: only one is True)
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight ahead?
            (dir_r and game.is_collision(pt_r)) or
            (dir_l and game.is_collision(pt_l)) or
            (dir_u and game.is_collision(pt_u)) or
            (dir_d and game.is_collision(pt_d)),

            # Danger to the right?
            (dir_u and game.is_collision(pt_r)) or
            (dir_d and game.is_collision(pt_l)) or
            (dir_l and game.is_collision(pt_u)) or
            (dir_r and game.is_collision(pt_d)),

            # Danger to the left?
            (dir_d and game.is_collision(pt_r)) or
            (dir_u and game.is_collision(pt_l)) or
            (dir_r and game.is_collision(pt_u)) or
            (dir_l and game.is_collision(pt_d)),

            # Current move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location relative to head
            game.food.x < game.head.x,  # food is to the left
            game.food.x > game.head.x,  # food is to the right
            game.food.y < game.head.y,  # food is above
            game.food.y > game.head.y   # food is below
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        """Store one experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """
        Learn from a random batch of past experiences.
        Called after every game — the main learning step.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """Learn from the single most recent experience (real-time learning)."""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """
        Decide what to do:
        - Early on (high epsilon): explore randomly
        - Later (low epsilon): exploit what we've learned
        This balance is called the exploration-exploitation tradeoff.
        """
        self.epsilon = 80 - self.n_games  # epsilon shrinks as more games are played

        action = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            # Random move — explore
            move = random.randint(0, 2)
            action[move] = 1
        else:
            # Predicted move — exploit
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction   = self.model(state_tensor)
            move         = torch.argmax(prediction).item()
            action[move] = 1

        return action
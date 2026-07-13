import matplotlib.pyplot as plt
from collections import deque
from agent import Agent
from snake_game import SnakeGameAI

# Live Plot Setup
plt.ion()  # interactive mode — updates the plot in real time

def plot(scores, mean_scores):
    """Plot scores and average scores as the agent trains."""
    plt.clf()
    plt.title('Snake RL Training Progress')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score per game')
    plt.plot(mean_scores, label='Average score')
    plt.legend()
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.pause(0.1)
    plt.show()


# Training Loop 
def train():
    scores      = []        # score from each game
    mean_scores = []        # running average
    total_score = 0
    record      = 0         # best score so far
    
    agent = Agent()
    game  = SnakeGameAI()

    print("Training started! Watch the snake learn...")
    print("Close the pygame window to stop training.\n")

    while True:
        # 1. Get current state
        state = agent.get_state(game)

        # 2. Decide action based on current state
        action = agent.get_action(state)

        # 3. Perform action and get feedback from the game
        reward, game_over, score = game.play_step(action)

        # 4. Get the new state after the action
        new_state = agent.get_state(game)

        # 5. Learn from this single step (short memory)
        agent.train_short_memory(state, action, reward, new_state, game_over)

        # 6. Remember this experience for later batch learning
        agent.remember(state, action, reward, new_state, game_over)

        if game_over:
            # 7. Game over — reset and train on a batch of past experiences
            game.reset()
            agent.n_games += 1

            # Long memory training (the main learning step)
            agent.train_long_memory()

            # Save the model if it beat the record
            if score > record:
                record = score
                agent.model.save()
                print(f"New record! Game {agent.n_games} | Score: {score} | Record: {record}")

            print(f"Game {agent.n_games} | Score: {score} | Record: {record}")

            # Track scores for plotting
            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)

            # Update the live plot
            plot(scores, mean_scores)


if __name__ == "__main__":
    train()
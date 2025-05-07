//Author: Allison Tang
//Modified by: Benjamin Steinberg
//Ben: added a win condition rather than going to just time

using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class Timer : MonoBehaviour
{
    public TextMeshProUGUI timerText; // Text field for displaying the timer
    public float timeLimit = 30f; // Timer set to 30 seconds
    public int winningScore = 6; // Set the score needed to win
    private float timeRemaining;
    private bool gameOver = false;
    public GameObject endScreen;
    public TextMeshProUGUI finalScoreText;
    public GameObject exitGameButton;
    public GameObject tryAgainButton;
    public ScoreManager scoreManager;
    public HeartSpawner heartSpawner;
    public bool gameStarted = false; // Track whether the game has started

    void Start()
    {
        timeRemaining = timeLimit;
        endScreen.SetActive(false);
        exitGameButton.SetActive(false);
        tryAgainButton.SetActive(false);
    }

    void Update()
    {
        if (!gameStarted || gameOver) return;

        // Update the timer countdown
        timeRemaining -= Time.deltaTime;

        // Update the timer text
        timerText.text = Mathf.Ceil(timeRemaining).ToString();

        // Check if player reached winning score
        if (scoreManager.GetScore() >= winningScore)
        {
            EndGame(true);
        }

        // Check if time has run out
        if (timeRemaining <= 0)
        {
            timeRemaining = 0;
            timerText.text = "0";
            EndGame(false);
        }
    }

    // Call this function when game starts
    public void StartGame()
    {
        timeRemaining = timeLimit;
        gameOver = false;
        gameStarted = true;

        timerText.text = Mathf.Ceil(timeRemaining).ToString();
        exitGameButton.SetActive(false);
        tryAgainButton.SetActive(false);
    }

    // Function to handle the end of the game
    private void EndGame(bool playerWon)
    {
        gameOver = true;
        heartSpawner.EndGame();
        endScreen.SetActive(true);

        if (playerWon)
        {
            finalScoreText.text = $"You Win! Final Score: {scoreManager.GetScore()}";
            exitGameButton.SetActive(true);
            Debug.Log("Win condition triggered!");
        }
        else
        {
            finalScoreText.text = $"Try Again! Get {winningScore} to win.\nYour Score: {scoreManager.GetScore()}";
            tryAgainButton.SetActive(true);
            Debug.Log("Game Over triggered!");
        }
    }

    public void TryAgain()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }
}


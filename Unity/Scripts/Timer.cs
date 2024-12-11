using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Timer : MonoBehaviour
{
    public TextMeshProUGUI timerText; // Text field for displaying the timer
    public float timeLimit = 30f; // Timer set to 30 seconds
    private float timeRemaining;
    private bool gameOver = false;
    public GameObject endScreen;
    public TextMeshProUGUI finalScoreText;
    public ScoreManager scoreManager;
    public HeartSpawner heartSpawner;
    public bool gameStarted = false; // Track whether the game has started

    void Start()
    {
        timeRemaining = timeLimit; // Initialize time remaining
        endScreen.SetActive(false);
    }

    void Update()
    {
        if (!gameStarted || gameOver) return; // If the game has not started do nothing

    // Update the timer countdown
    timeRemaining -= Time.deltaTime;

    // Update the timer text
    timerText.text = Mathf.Ceil(timeRemaining).ToString();

    // Check if time has run out
    if (timeRemaining <= 0)
    {
        timeRemaining = 0;
        timerText.text = "0"; // Show 0 when the time runs out
        EndGame(); // Call the function to end the game
    }
    }

    // Call this function when game starts
    public void StartGame()
    {
        timeRemaining = timeLimit; // Reset the timer to its starting value
        gameOver = false; // Ensure the game isn't over when starting
        gameStarted = true; // Set gameStarted to true when the game starts

        // Update the timerText immediately when the game starts
    timerText.text = Mathf.Ceil(timeRemaining).ToString(); // Update text to show 30 seconds initially
    }

    // Function to handle the end of the game
    private void EndGame()
    {
        gameOver = true;
        heartSpawner.EndGame(); // Stop spawning hearts
        Debug.Log("Game Over triggered!");

        endScreen.SetActive(true);

        // Display the final score
        finalScoreText.text = $"Final Score: { scoreManager.GetScore()}";
    }
}

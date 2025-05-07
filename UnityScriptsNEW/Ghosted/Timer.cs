//Author: Allison Tang

using System.Collections;
using UnityEngine;
using TMPro;

public class GhostTimer : MonoBehaviour
{
    public GhostGameManager gameManager;

    public TextMeshProUGUI timerText;
    public float timeLimit = 30f;
    private float timeRemaining;
    private bool gameOver = false;

    public GameObject endScreen;
    public bool gameStarted = false;

    void Start(){
        timeRemaining = timeLimit;
        timerText.text = "";
        endScreen.SetActive(false);
    }

    void Update(){
        if (!gameStarted || gameOver) return;

        timeRemaining -= Time.deltaTime;
        timerText.text = $"Time: {Mathf.Ceil(timeRemaining)}";

        if (timeRemaining <= 0){
            timeRemaining = 0;
            timerText.text = "Time: 0";
            EndGame();
        }
    }

    public void ResetAndStartTimer(){
        timeRemaining = timeLimit;
        gameOver = false;
        gameStarted = true;
        timerText.text = $"Time: {Mathf.Ceil(timeRemaining)}";
    }

    public void StartGame(){
        timeRemaining = timeLimit;
        gameOver = false;
        gameStarted = true;
        endScreen.SetActive(false);
        timerText.text = $"Time: {Mathf.Ceil(timeRemaining)}";
    }

    private void EndGame()
{
    gameOver = true;
    gameStarted = false;

    endScreen.SetActive(true);   
    gameManager.GameOver(); 

    //FindObjectOfType<ExitOnClick>().AllowExit();

    Debug.Log("Time ran out");
    }
}

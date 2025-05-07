//Author: Allison Tang

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;

public class GhostGameManager : MonoBehaviour, IGameStateProvider
{
    public Image targetGhostDisplay;
    public RectTransform ghostSpawnArea;
    public GameObject startScreen;
    public GameObject winScreen;
    public GameObject roundPanel;
    public TextMeshProUGUI roundLabel;

    public GameObject ghostButtonPrefab;
    public List<Sprite> ghostSprites;

    public int currentRound = 1;
    public int maxRounds = 3;

    public int baseGhostCount = 10;
    public float baseSpeed = 50f;
    public float speedIncrease = 25f;
    public int ghostIncrease = 5;

    public GhostTimer timer;

    private string targetGhostID;
    private bool gameStarted = false;
    private bool gameOver = false;

    public AudioClip correctGhostSound;
    private AudioSource audioSource;

    void Start()
    {
        startScreen.SetActive(true);
        winScreen.SetActive(false);
        roundPanel.SetActive(false);
        audioSource = GetComponent<AudioSource>();
    }

    public void StartGame()
    {
        startScreen.SetActive(false);
        gameStarted = true;
        StartCoroutine(HandleRoundTransition());
    }

    public void CheckGhost(string clickedID)
    {
        if (!gameStarted || gameOver) return;

        if (clickedID == targetGhostID)
        {
            if (correctGhostSound != null)
                audioSource.PlayOneShot(correctGhostSound);

            currentRound++;

            if (currentRound > maxRounds)
            {
                EndGame();
            }
            else
            {
                StartCoroutine(HandleRoundTransition());
            }
        }
        else
        {
            Debug.Log("Wrong ghost");
        }
    }

    public void StartNewRound()
    {
        if (gameOver) return;

        foreach (Transform child in ghostSpawnArea)
        {
            Destroy(child.gameObject);
        }

        int targetIndex = Random.Range(0, ghostSprites.Count);
        targetGhostID = "Ghost_" + targetIndex;
        targetGhostDisplay.sprite = ghostSprites[targetIndex];

        int ghostCount = baseGhostCount + ghostIncrease * (currentRound - 1);
        float ghostSpeed = baseSpeed + speedIncrease * (currentRound - 1);
        int correctGhostSlot = Random.Range(0, ghostCount);

        for (int i = 0; i < ghostCount; i++)
        {
            int spriteIndex = (i == correctGhostSlot)
                ? targetIndex
                : Random.Range(0, ghostSprites.Count);

            while (i != correctGhostSlot && spriteIndex == targetIndex)
            {
                spriteIndex = Random.Range(0, ghostSprites.Count);
            }

            GameObject ghost = Instantiate(ghostButtonPrefab, ghostSpawnArea);
            ghost.GetComponent<GhostButton>().Init(
                "Ghost_" + spriteIndex,
                ghostSprites[spriteIndex],
                this
            );

            RectTransform rt = ghost.GetComponent<RectTransform>();
            rt.anchoredPosition = new Vector2(
                Random.Range(-400f, 400f),
                Random.Range(-600f, 600f)
            );

            GhostDrifter drifter = ghost.GetComponent<GhostDrifter>();
            if (drifter != null)
            {
                drifter.speed = ghostSpeed;
                drifter.gameManager = this;
            }
        }
    }

    private IEnumerator HandleRoundTransition()
    {
        roundPanel.SetActive(true);
        roundLabel.gameObject.SetActive(true);

        if (currentRound == maxRounds)
            roundLabel.text = "FINAL ROUND!";
        else
            roundLabel.text = $"ROUND {currentRound}";

        CanvasGroup cg = roundLabel.GetComponent<CanvasGroup>();
        if (cg == null)
            cg = roundLabel.gameObject.AddComponent<CanvasGroup>();

        cg.alpha = 0;
        float fadeDuration = 0.5f;

        while (cg.alpha < 1f)
        {
            cg.alpha += Time.deltaTime / fadeDuration;
            yield return null;
        }

        yield return new WaitForSeconds(1.5f);

        while (cg.alpha > 0f)
        {
            cg.alpha -= Time.deltaTime / fadeDuration;
            yield return null;
        }

        roundLabel.gameObject.SetActive(false);
        roundPanel.SetActive(false);

        StartNewRound();
        timer.ResetAndStartTimer();
    }

    private void EndGame()
    {
        gameOver = true;
        timer.gameStarted = false;
        winScreen.SetActive(true);
        //FindObjectOfType<ExitOnClick>().AllowExit();
    }

    public void GameOver()
    {
        gameOver = true;
        timer.gameStarted = false;
    }

    public bool IsGameOver()
    {
        return gameOver;
    }

    public void RestartGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GH_GameManager : MonoBehaviour, IGameStateProvider
{
    public static GH_GameManager instance;

    [Header("Ghost Settings")]
    public GameObject ghostPrefab;
    public int maxGhosts = 7;
    public float spawnInterval = 2f;
    public string[] toxicSayings;
    public Sprite[] ghostSprites;
    public GameObject sayingBubblePrefab;

    [Header("UI Elements")]
    public TMP_Text timerText;
    public TMP_Text ghostsLeftText;

    [Header("Game Settings")]
    public float timeLimit = 30f;
    private float timer;
    private float spawnTimer;
    public int ghostsToWin = 10;
    private int ghostsTapped = 0;
    private bool gameActive = true;
    private List<GameObject> activeGhosts = new List<GameObject>();
    
    [Header("Start UI")]
    public GameObject startButton;
    public GameObject exitButton;
    public GameObject startOverlay;
    public TMP_Text overlayMessageText;

    [Header("Audio Settings")]
    public AudioSource backgroundMusic;
    public AudioSource ghostTapSource;


    void Awake()
    {
        instance = this;
    }

    void Start()
    {
        gameActive = false;
    }

    void Update()
    {
        if (!gameActive) return;

        timer -= Time.deltaTime;
        timerText.text = "" + Mathf.Ceil(timer);

        if (timer <= 0)
        {
            EndGame(false);
        }

        spawnTimer += Time.deltaTime;
        if (spawnTimer >= spawnInterval && activeGhosts.Count < maxGhosts && ghostsTapped + activeGhosts.Count < ghostsToWin)
        {
            spawnTimer = 0;
            spawnInterval = Random.Range(0.2f, 2f);
            SpawnGhost();
        }
    }

    void SpawnGhost()
    {
        Vector2 spawnPos = GetRandomWorldPosition();
        GameObject ghost = Instantiate(ghostPrefab, spawnPos, Quaternion.identity);
        ghost.transform.localScale *= Random.Range(1.5f, 2.5f);

        SpriteRenderer sr = ghost.GetComponentInChildren<SpriteRenderer>();

        if (sr == null)
        {
            Debug.LogWarning("No SpriteRenderer found on ghost prefab!");
        }
        else if (ghostSprites == null || ghostSprites.Length == 0)
        {
            Debug.LogWarning("ghostSprites array is empty or not assigned!");
        }
        else
        {
            int index = Random.Range(0, ghostSprites.Length);
            sr.sprite = ghostSprites[index];
            Debug.Log($"Assigned ghost sprite: {ghostSprites[index].name}");
        }

        ghost.AddComponent<Ghost>();
        activeGhosts.Add(ghost);
    }

    Vector2 GetRandomWorldPosition()
    {
        float padding = 0.1f;
        float x = Random.Range(padding, 1 - padding);
        float y = Random.Range(padding, 1 - padding);
        Vector2 viewportPos = new Vector2(x, y);
        Vector2 worldPos = Camera.main.ViewportToWorldPoint(viewportPos);
        return worldPos;
    }

    public void GhostTapped(Vector3 ghostPosition, GameObject ghost)
    {
        ghostsTapped++;
        ghostsLeftText.text = $"{ghostsTapped}/{ghostsToWin}";

        if (ghostTapSource != null)
        {
            ghostTapSource.Play();
        }

        string phrase = toxicSayings[Random.Range(0, toxicSayings.Length)];

        if (sayingBubblePrefab != null)
        {
            Vector3 screenPos = Camera.main.WorldToScreenPoint(ghostPosition);
            Vector3 offset;

            // Check for upper-right corner
            bool tooHigh = screenPos.y > Screen.height * 0.75f;
            bool tooRight = screenPos.x > Screen.width * 0.75f;

            if (tooHigh && tooRight)
            {
                offset = new Vector3(-2.0f, -.5f, 0f); // spawn to the left
            }
            else if (tooHigh)
            {
                offset = new Vector3(2.0f, -.5f, 0f); // spawn to the right
            }
            else
            {
                offset = new Vector3(1.3f, 1.3f, 0f); // normal top-right
            }

            Vector3 offsetPosition = ghostPosition + offset;
            GameObject bubble = Instantiate(sayingBubblePrefab, offsetPosition, Quaternion.identity);
            bubble.transform.rotation = Quaternion.identity;
            bubble.GetComponentInChildren<TMPro.TextMeshPro>().text = phrase;

            StartCoroutine(FadeOutAndDestroy(ghost, bubble));
        }
        else
        {
            Destroy(ghost);
        }

        RemoveGhost(ghost);

        if (ghostsTapped >= ghostsToWin)
        {
            EndGame(true);
        }
    }


    private IEnumerator FadeOutAndDestroy(GameObject ghost, GameObject bubble)
    {
        float duration = 2.5f;
        float elapsed = 0f;

        //Find the SpriteRenderer and TextMeshPro inside children
        SpriteRenderer ghostRenderer = ghost.GetComponentInChildren<SpriteRenderer>();
        SpriteRenderer bubbleRenderer = bubble.GetComponentInChildren<SpriteRenderer>();
        TextMeshPro bubbleText = bubble.GetComponentInChildren<TextMeshPro>();

        // Default to white if any component is missing (prevents null errors on .color)
        Color ghostColor = ghostRenderer != null ? ghostRenderer.color : Color.white;
        Color bubbleColor = bubbleRenderer != null ? bubbleRenderer.color : Color.white;
        Color textColor = bubbleText != null ? bubbleText.color : Color.white;

        while (elapsed < duration)
        {
            float t = 1f - (elapsed / duration);

            if (ghostRenderer != null)
                ghostRenderer.color = new Color(ghostColor.r, ghostColor.g, ghostColor.b, t);

            if (bubbleRenderer != null)
                bubbleRenderer.color = new Color(bubbleColor.r, bubbleColor.g, bubbleColor.b, t);

            if (bubbleText != null)
                bubbleText.color = new Color(textColor.r, textColor.g, textColor.b, t);

            elapsed += Time.deltaTime;
            yield return null;
        }

        Destroy(ghost);
        Destroy(bubble);
    }

    public void RemoveGhost(GameObject ghost)
    {
        if (activeGhosts.Contains(ghost))
        {
            activeGhosts.Remove(ghost);
        }
    }

    void EndGame(bool win)
    {
        gameActive = false;
        spawnTimer = 0f;

        if (!win)
        {
            foreach (GameObject ghost in activeGhosts)
            {
                if (ghost != null)
                    Destroy(ghost);
            }
            activeGhosts.Clear();
        }

        if (startOverlay != null) startOverlay.SetActive(true);
        if (startButton != null && !win) startButton.SetActive(true);
        if (exitButton != null) exitButton.SetActive(true);
        
        if (overlayMessageText != null)
            overlayMessageText.text = win ? "You Win!" : "You failed... Try again";

        if (backgroundMusic != null) backgroundMusic.Stop();

    }

    public void StartGame()
    {
        timer = timeLimit;
        ghostsTapped = 0;
        ghostsLeftText.text = $"0/{ghostsToWin}";
        gameActive = true;

        if (startButton != null) startButton.SetActive(false);
        if (startOverlay != null) startOverlay.SetActive(false);
        if (exitButton != null) exitButton.SetActive(false);

        timerText.text = $"{timeLimit}";
        ghostsLeftText.text = $"0/{ghostsToWin}";

        if (backgroundMusic != null)
            backgroundMusic.Play();
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }

}
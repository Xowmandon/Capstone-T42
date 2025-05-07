//Author: Benjamin Steinberg
//Created on: 4/25/2025

using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class IckWipe : MonoBehaviour, IGameStateProvider
{
    [Header("Ick Setup")]
    public Image ickImage;
    public Sprite[] ickSprites;

    [Header("Scrub Settings")]
    public float scrubGoal = 100f;
    public float scrubSpeed = 1f;

    [Header("UI References")]
    public Camera uiCamera;
    public RectTransform soapBar;
    public GameObject bubbleEffectPrefab;
    public Slider scrubProgressBar;
    public GameObject startScreen;
    public GameObject endScreen;
    public Button startButton;

    [Header("Audio")]
    public AudioSource squeakAudio;
    private bool isPlayingSqueak = false;

    private float currentScrub = 0f;
    private bool gameStarted = false;

    void Start()
    {
        startScreen.SetActive(true);
        endScreen.SetActive(false);

        startButton.onClick.AddListener(StartGame);
    }

    void StartGame()
    {
        gameStarted = true;
        startScreen.SetActive(false);

        if (ickSprites.Length > 0)
        {
            int index = Random.Range(0, ickSprites.Length);
            ickImage.sprite = ickSprites[index];
        }

        ickImage.gameObject.SetActive(true);
        if (soapBar != null) soapBar.gameObject.SetActive(false);

        if (scrubProgressBar != null)
        {
            scrubProgressBar.minValue = 0;
            scrubProgressBar.maxValue = scrubGoal;
            scrubProgressBar.value = 0;
            scrubProgressBar.gameObject.SetActive(true);
        }
    }

    void Update()
    {
        if (!gameStarted) return;

        Vector2 inputPos = Vector2.zero;
        bool isScrubbing = false;

        if (Input.GetMouseButton(0))
        {
            inputPos = Input.mousePosition;
            isScrubbing = true;
        }
        else if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            inputPos = touch.position;
            if (touch.phase == TouchPhase.Moved || touch.phase == TouchPhase.Stationary)
                isScrubbing = true;
        }

        if (isScrubbing)
        {
            if (soapBar != null)
            {
                soapBar.gameObject.SetActive(true);
                RectTransformUtility.ScreenPointToLocalPointInRectangle(
                    soapBar.parent as RectTransform, inputPos, uiCamera, out Vector2 localPoint);
                soapBar.localPosition = localPoint;
            }

            if (RectTransformUtility.RectangleContainsScreenPoint(ickImage.rectTransform, inputPos, uiCamera))
            {
                currentScrub += scrubSpeed * Time.deltaTime * 100;

                if (!isPlayingSqueak)
                {
                    squeakAudio.Play();
                    isPlayingSqueak = true;
                }

                if (bubbleEffectPrefab != null)
                {
                    Instantiate(bubbleEffectPrefab, inputPos, Quaternion.identity, ickImage.canvas.transform);
                }

                if (scrubProgressBar != null)
                    scrubProgressBar.value = currentScrub;

                if (currentScrub >= scrubGoal)
                {
                    squeakAudio.Stop();
                    ickImage.gameObject.SetActive(false);
                    if (soapBar != null) soapBar.gameObject.SetActive(false);
                    if (scrubProgressBar != null) scrubProgressBar.gameObject.SetActive(false);
                    endScreen.SetActive(true);
                    gameStarted = false;
                }
            }
        }
        else
        {
            if (soapBar != null) soapBar.gameObject.SetActive(false);

            if (isPlayingSqueak)
            {
                squeakAudio.Stop();
                isPlayingSqueak = false;
            }
        }
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }

}
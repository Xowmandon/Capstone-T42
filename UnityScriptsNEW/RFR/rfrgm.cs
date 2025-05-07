//Author: Benjamin Steinberg
//Created on: 12/11/24

using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using TMPro;

[System.Serializable]
public struct RFRGameState
{
    public bool[] answers;// 5 rounds
    public string[] prompt;
    public int masterSeed;
}

public class rfrgm : MonoBehaviour, IGameStateProvider
{
    [Header("Game Screens")]
    public GameObject startScreen;
    public Button startButton;
    public GameObject exitScreen;

    [Header("Buttons & UI")]
    public Button[] buttonArr;
    public DialogueManager dialogueManager;

    [Header("Prompt & Game Data")]
    public promptHandler promptHandler;
    private int[] roundSeeds = new int[5];
    private int masterSeed;

    [Header("Car & Audio")]
    public GameObject car;
    public AudioSource audioHandler;
    public AudioClip carStop;
    public AudioClip carFinalStop;
    public AudioClip engineNoise;

    // Private State
    private int roundNum = 0;
    private bool isActive;
    private string[] loadedPrompts = new string[5];
    private int[] usedSeeds = new int[5];
    private bool[] picks = new bool[5];

    void Awake()
    {
        buttonSetup();
        startScreen.SetActive(true);
        exitScreen.SetActive(false);
        startButton.onClick.AddListener(StartGame);
        SetButtonsInteractable(false);
        if (!string.IsNullOrEmpty(SceneTransfer.rawJson))
        {
            LoadFullGameStateFromJSON(SceneTransfer.rawJson);
        }
    }

    void Start()
    {
        LoadFullGameStateFromJSON(SceneTransfer.rawJson);
    }

    void StartGame()
    {
        startScreen.SetActive(false);
        dialogueManager.EnqueueDialogue(new DialogueEntry("Pick if these prompts are a red or green flag", null, () =>
        {
            roundReset();
        }));
    }

    void buttonSetup()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            var btn = buttonArr[i].GetComponentInParent<inGameButton>();
            btn.SetGameManRef(this);
            btn.setButton((i != 0));
        }
    }

    void roundReset()
    {
        dialogueManager.EnqueueDialogue(new DialogueEntry("Driving..."));
        StartCoroutine(isDriving());
        isActive = false;
        SetButtonsInteractable(false);
    }

    void SetButtonsInteractable(bool active)
    {
        foreach (var btn in buttonArr)
        {
            btn.interactable = active;
        }
    }

    private IEnumerator isDriving()
    {
        if (car == null)
        {
            Debug.LogError("Car reference is not assigned!");
            yield break;
        }

        Vector3 originalPosition = car.transform.position;
        float shakeDuration = UnityEngine.Random.Range(4.0f, 6.0f);
        float elapsedTime = 0f;
        float shakeAmount = 0.04f;

        audioHandler.PlayOneShot(engineNoise);

        while (elapsedTime < shakeDuration)
        {
            float shakeX = Random.Range(-shakeAmount, shakeAmount);
            car.transform.position = new Vector3(originalPosition.x + shakeX, originalPosition.y, originalPosition.z);
            elapsedTime += Time.deltaTime;
            yield return null;
        }

        car.transform.position = originalPosition;

        audioHandler.Stop();
        audioHandler.PlayOneShot(roundNum < 5 ? carStop : carFinalStop);

        if (roundNum == 5)
        {
            endGame();
        }
        else
        {
            callPrompt();
        }
    }

    public void getAnswer(bool answer)
    {
        if (isActive)
        {
            picks[roundNum] = answer;
            roundNum++;
            roundReset();
        }
    }

    void endGame()
    {
        isActive = false;
        SetButtonsInteractable(false);
        audioHandler.PlayOneShot(carFinalStop);
        dialogueManager.EnqueueDialogue(new DialogueEntry("You have arrived at Chili's", null, () => exitScreen.SetActive(true)));
    }

    void callPrompt()
    {
        string prompt;

        if (!string.IsNullOrEmpty(loadedPrompts[roundNum]))
        {
            prompt = loadedPrompts[roundNum];
        }
        else
        {
            int seed = roundSeeds[roundNum];
            usedSeeds[roundNum] = seed;
            UnityEngine.Random.InitState(seed);

            if (promptHandler != null)
            {
                prompt = promptHandler.GetRandomPrompt();
            }
            else
            {
                Debug.LogError("promptHandler is not assigned!");
                prompt = "Missing prompt handler — please assign it in the Inspector.";
            }

            loadedPrompts[roundNum] = prompt;
        }

        dialogueManager.EnqueueDialogue(new DialogueEntry(prompt));
        isActive = true;
        SetButtonsInteractable(true);
    }

    public string GetGameStateJSON()
    {
        RFRGameState state = new RFRGameState
        {
            answers = picks,
            prompt = loadedPrompts,
            masterSeed = masterSeed
        };
        return JsonUtility.ToJson(state);
    }

    public void LoadFullGameStateFromJSON(string json)
    {
        if (string.IsNullOrWhiteSpace(json) || json.Trim() == "{}")
        {
            Debug.Log("Starting Red Flag Racing with default values.");
            int fallbackSeed = UnityEngine.Random.Range(0, 10000);
            InitializeRoundSeeds(fallbackSeed);
            return;
        }

        RFRGameState state = JsonUtility.FromJson<RFRGameState>(json);
        masterSeed = state.masterSeed;
        InitializeRoundSeeds(masterSeed);

        picks = state.answers ?? new bool[5];
        loadedPrompts = state.prompt ?? new string[5];
    }

    public void InitializeRoundSeeds(int seedFromAPI)
    {
        masterSeed = seedFromAPI;
        System.Random seedGen = new System.Random(masterSeed);
        for (int i = 0; i < 5; i++)
        {
            roundSeeds[i] = seedGen.Next(0, 10000);
        }
    }
}

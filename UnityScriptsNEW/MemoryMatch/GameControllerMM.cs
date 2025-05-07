//Author: Benjamin Steinberg
//Created on: 12/8/2024

using UnityEngine;
using TMPro;
using UnityEngine.UI;
using System.Collections;

public class GameControllerMM : MonoBehaviour, IGameStateProvider
{
    [Header("Game UI")]
    public TMP_Text[] buttonArr;
    public TMP_Text scoreboardText;

    [Header("Game Screens")]
    public GameObject startScreen;
    public Button startButton;
    public GameObject exitScreen;

    [Header("Interests")]
    public string[] interests;
    public string[] fakeInterests;

    [HideInInspector]
    public bool canCheckCards = true;

    private MMCard currentSelect = null;
    private int score = 4;

    void Awake()
    {
        // Show start screen and hide other elements
        startScreen.SetActive(true);
        exitScreen.SetActive(false);
        scoreboardText.text = "";
        SetCardsInteractable(false);
    }

    void Start()
    {
        startButton.onClick.AddListener(StartGame);  
    }

    public void StartGame()
    {
        startScreen.SetActive(false);
        scoreboardText.text = "Matches Left: 4";
        AssignInterestsToButtons();
        SetGameContrRefonButt();
        SetCardsInteractable(true);
    }

    void AssignInterestsToButtons()
    {
        int[] indexes = new int[12];
        for (int i = 0; i < indexes.Length; i++) indexes[i] = i;
        ShuffleArray(indexes);

        int indexCounter = 0;
        for (int i = 0; i < 4; i++)
        {
            buttonArr[indexes[indexCounter++]].text = interests[i];
            buttonArr[indexes[indexCounter++]].text = interests[i];
        }

        for (int i = 0; i < 4; i++)
        {
            buttonArr[indexes[indexCounter++]].text = fakeInterests[i];
        }
    }

    void ShuffleArray(int[] array)
    {
        for (int i = array.Length - 1; i > 0; i--)
        {
            int rand = Random.Range(0, i + 1);
            int temp = array[i];
            array[i] = array[rand];
            array[rand] = temp;
        }
    }

    public void buttonClicked(MMCard button)
    {
        if (!canCheckCards) return;

        if (currentSelect == null)
        {
            currentSelect = button;
        }
        else
        {
            canCheckCards = false;
            StartCoroutine(HandleCardComparisonWithDelay(button));
        }
    }

    void updateScore()
    {
        score--;
        scoreboardText.text = "Matches Left: " + score;
        if (score == 0) gameover();
    }

    void gameover()
    {
        SetCardsInteractable(false);
        foreach (TMP_Text txt in buttonArr)
            txt.GetComponentInParent<MMCard>().reveal();

        exitScreen.SetActive(true);
    }

    void SetGameContrRefonButt()
    {
        foreach (TMP_Text txt in buttonArr)
            txt.GetComponentInParent<MMCard>().SetGameContrRef(this);
    }

    void SetCardsInteractable(bool interactable)
    {
        foreach (TMP_Text txt in buttonArr)
            txt.GetComponentInParent<Button>().interactable = interactable;
    }

    private IEnumerator HandleCardComparisonWithDelay(MMCard button)
    {
        yield return new WaitForSeconds(1f);

        if (button.buttonText.text == currentSelect.buttonText.text)
        {
            currentSelect.matched();
            button.matched();
            updateScore();
        }
        else
        {
            currentSelect.resetButton();
            button.resetButton();
        }

        currentSelect = null;
        canCheckCards = true;
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }
}

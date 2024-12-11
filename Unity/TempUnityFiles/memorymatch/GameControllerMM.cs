//Created by: Benjamin Steinberg
//Date Created: 12/10
//Updates: Need to fully implement with the app, import interests and stuff too


using UnityEngine;
using TMPro;
using UnityEngine.UI;
using Unity.VisualScripting;
using System.Net.Sockets;
using System.Collections;

public class GameControllerMM : MonoBehaviour
{
    //Public
    public TMP_Text[] buttonArr;
    public TMP_Text scoreboardText;
    public GameObject exitButton;
    public string[] interests;
    public string[] fakeInterests;
    public bool canCheckCards = true;
    
    //Private
    private MMCard currentSelect = null;
    private int score = 4;

    void Awake()
    {
        AssignInterestsToButtons();
        SetGameContrRefonButt();
        exitButton.SetActive(false);
    }

    void AssignInterestsToButtons()
    {
        // Create an array of indexes for buttonArr
        int[] indexes = new int[12];
        for (int i = 0; i < indexes.Length; i++)
        {
            indexes[i] = i;
        }

        // Shuffle the indexes
        ShuffleArray(indexes);

        int indexCounter = 0;

        // Assign interests to two different random locations
        for (int i = 0; i < 4; i++)
        {
            buttonArr[indexes[indexCounter++]].text = interests[i];
            buttonArr[indexes[indexCounter++]].text = interests[i];
        }

        // Assign fake interests to one different random locations
        for (int i = 0; i < 4; i++)
        {
            buttonArr[indexes[indexCounter++]].text = fakeInterests[i];
        }
    }

    void ShuffleArray(int[] array)
    {
        for (int i = array.Length - 1; i > 0; i--)
        {
            int randomIndex = Random.Range(0, i + 1);

            int temp = array[i];
            array[i] = array[randomIndex];
            array[randomIndex] = temp;
        }
    }

    public void buttonClicked(MMCard button)
    {
        if (currentSelect == null)
        {
            currentSelect = button;
        }

        else
        {
            Debug.Log("test");
            canCheckCards = false;
            StartCoroutine(HandleCardComparisonWithDelay(button));
        }

    }

    void updateScore()
    {
        score--;

        if(score == 0)
        {
            gameover();
            scoreboardText.text = "Matches Left: " + score;
        }
    }

    void gameover()
    {
        for(int i = 0; i < 12; i++)
        {
            buttonArr[i].gameObject.GetComponentInParent<MMCard>().reveal();
        }
        exitButton.SetActive(true);
    }
    void SetGameContrRefonButt()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            buttonArr[i].GetComponentInParent<MMCard>().SetGameContrRef(this);
        }
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
        Debug.Log("test2");
    }
}
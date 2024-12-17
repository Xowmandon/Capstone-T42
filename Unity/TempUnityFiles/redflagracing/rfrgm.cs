//Author: Benjamin Steinberg
//Created: 12/11/2024
//Notes: add road animation, add car asset, add nicer assets all around


using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using TMPro;

public class rfrgm : MonoBehaviour
{
    //Public
    public Button[] buttonArr;
    public TMP_Text activePrompt;
    public GameObject exitButton;
    public promptHandler prompts;
    public GameObject car;
    public bool[] picks;

    //Private
    private int roundNum = 0;
    private bool isActive;

    void buttonSetup()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            buttonArr[i].GetComponentInParent<inGameButton>().SetGameManRef(this);
            buttonArr[i].GetComponentInParent<inGameButton>().setButton((i != 0));
        }
    }

    void Awake()
    {
        buttonSetup();
        exitButton.SetActive(false);
        roundReset();
        StartCoroutine(isDriving());
    }

    private IEnumerator isDriving()
    {
        if (car == null)
        {
            Debug.LogError("Car reference is not assigned!");
            yield break;
        }

        // Store the original position of the car
        Vector3 originalPosition = car.transform.position;

        // Shake parameters
        float shakeDuration = 2f;  // Duration of shake
        float shakeAmount = 0.1f;  // How much to shake
        float elapsedTime = 0f;

        // Perform the shake
        while (elapsedTime < shakeDuration)
        {
            float shakeX = Random.Range(-shakeAmount, shakeAmount);
            car.transform.position = new Vector3(originalPosition.x + shakeX, originalPosition.y, originalPosition.z);
            elapsedTime += Time.deltaTime;

            // Wait until the next frame
            yield return null;
        }

        car.transform.position = originalPosition;
        callPrompt();
    }

    void setActivePrompt(string prompt)
    {
        activePrompt.text = prompt;
    }

    public void getAnswer(bool answer)
    {
        if(isActive)
        {
            picks[roundNum] = answer;
            roundNum++;
            if(roundNum == 5)
            {
                endGame();
            }
            else{
                roundReset();
                StartCoroutine(isDriving());
            }
        }
    }

    void endGame()
    {
        exitButton.SetActive(true);
        setActivePrompt("You have arrived at Chili's");
    }

    void roundReset()
    {
        setActivePrompt("Driving...");
        isActive = false;
    }

    void callPrompt()
    {
        setActivePrompt(prompts.GetRandomPrompt());
        isActive = true;
    }
}
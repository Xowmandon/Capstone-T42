using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class GameManager : MonoBehaviour
{
public GameObject startButton; // Reference to the Start Button
public HeartSpawner heartSpawner;

    public void StartGame()
    {
        startButton.SetActive(false); // Hide the Start Button
    }

    void EndGame()
{
    heartSpawner.EndGame(); // Call the EndGame method in the HeartSpawner script
}

}

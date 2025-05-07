//Author: Benjamin Steinberg
//Date Created: 4/20/2025

using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;

public class CatchTheGhostGame : MonoBehaviour, IGameStateProvider
{
    [Header("UI Panels")]
    public GameObject startScreen;
    public GameObject winScreen;

    [Header("Gameplay")]
    public GameObject ghost;
    public AudioSource ghostLaugh;

    [Header("Text")]
    public TMP_Text ghostMessageText;

    private int tapCount = 0;
    private int tapsToCatch;
    private bool gameActive = false;

    private List<string> ghostTaunts = new List<string>
    {
        "Haha you almost got me!",
        "Too slow!",
        "Catch me if you can!",
        "You call that a tap?",
        "Ghost mode: activated!",
        "Is that all you've got?",
        "Not even close!",
        "Spooky fast, aren’t I?",
        "Oops, missed again!",
        "Boo-hoo, not this time!"
    };

    void Start()
    {
        startScreen.SetActive(true);
        winScreen.SetActive(false);
        ghost.SetActive(false);
        ghostMessageText.text = "";
    }

    public void StartGame()
    {
        startScreen.SetActive(false);
        winScreen.SetActive(false);
        tapsToCatch = Random.Range(5, 11); // 5 to 10 taps needed
        tapCount = 0;
        gameActive = true;
        ghost.SetActive(true);
        MoveGhost();
        ghostMessageText.text = "";
    }

    public void TapGhost()
    {
        if (!gameActive) return;

        tapCount++;

        if (tapCount >= tapsToCatch)
        {
            StartCoroutine(EndGame());
        }
        else
        {
            StartCoroutine(RespawnGhost());
        }
    }

    IEnumerator RespawnGhost()
    {
        ghost.SetActive(false);
        if (ghostLaugh) ghostLaugh.Play();

        string randomTaunt = ghostTaunts[Random.Range(0, ghostTaunts.Count)];
        ghostMessageText.text = randomTaunt;

        yield return new WaitForSeconds(0.7f);
        MoveGhost();
        ghost.SetActive(true);
    }

    void MoveGhost()
    {
        Vector2 screenSize = new Vector2(Screen.width, Screen.height);
        Vector2 worldPos = Camera.main.ScreenToWorldPoint(new Vector2(Random.Range(0, screenSize.x), Random.Range(0, screenSize.y)));
        ghost.transform.position = new Vector3(worldPos.x, worldPos.y, 0);
    }

    IEnumerator EndGame()
    {
        gameActive = false;
        ghost.SetActive(false);
        ghostMessageText.text = "";
        yield return new WaitForSeconds(1f);
        winScreen.SetActive(true);
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }

}
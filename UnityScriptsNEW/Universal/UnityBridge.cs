// Handles communication from Unity to Swift via Objective-C bridge.
// Sends full game state JSON to host after every turn or at game over.

//Author: Benjamin Steinberg
//Date Created: 4/19/25

using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.UI;

public class UnityGameBridge : MonoBehaviour
{
    public Button exitButton;
    public MonoBehaviour gameLogic;

    private IGameStateProvider gameStateProvider;

#if UNITY_IOS && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern void sendGameSaveDataToHost(string json);
#endif

    private void Start()
    {
        gameStateProvider = gameLogic as IGameStateProvider;

        if (exitButton != null)
        {
            exitButton.onClick.AddListener(OnExitClicked);
        }

        if (gameStateProvider == null)
        {
            Debug.LogError("[UnityGameBridge] Attached component doesn't implement IGameStateProvider!");
        }
    }

    private void OnExitClicked()
    {
        if (gameStateProvider != null)
        {
            NotifySwiftGameState(gameStateProvider.GetGameStateJSON());
        }
        else
        {
            Debug.LogWarning("[UnityGameBridge] GameStateProvider not set or invalid.");
        }
    }

    public static void NotifySwiftGameState(string gameJson)
    {
#if UNITY_IOS && !UNITY_EDITOR
        sendGameSaveDataToHost(gameJson);
#else
        Debug.Log($"[DEBUG] Would sendGameSaveDataToHost({gameJson})");
#endif
    }
}
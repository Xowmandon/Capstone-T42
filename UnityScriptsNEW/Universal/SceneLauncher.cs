//Author: Benjamin Steinberg
//Created on: 4/19/25

using UnityEngine;
using UnityEngine.SceneManagement;
using System.Runtime.InteropServices;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


//general boiler plate function, grabbed mostly from article
public static class SceneTransfer
{
    public static string rawJson;
}

public class SceneLauncher : MonoBehaviour
{
#if UNITY_IOS && !UNITY_EDITOR
    [DllImport("__Internal")] //looks inside app's native code (swift) for this function
    public static extern void didFinishLoadingInstance(); //This function is implemented outside, simple declaration
#endif

    void Start()
    {
#if UNITY_IOS && !UNITY_EDITOR
        didFinishLoadingInstance();
#endif

        // Stringified JSON example
        
        string nestedJson = "{\"game_name\":\"TicTacToe\",\"game_state\":\"{\\\"boardState\\\":[\\\"X\\\",\\\"\\\",\\\"\\\",\\\"\\\",\\\"O\\\",\\\"\\\",\\\"\\\",\\\"\\\",\\\"X\\\"],\\\"nameP1\\\":\\\"Harry Sho\\\",\\\"winner\\\":\\\"\\\",\\\"nameP2\\\":\\\"DEBUG\\\",\\\"playerNum\\\":0}\"}";

        LaunchGameFromJSON(nestedJson);
        
    }

    public void LaunchGameFromJSON(string json)
    {
        JObject outer = JObject.Parse(json);
        string sceneName = outer["game_name"]?.ToString();

        // Always expect game_state as string and parse it
        string gameStateStr = outer["game_state"]?.ToString();
        if (!string.IsNullOrEmpty(gameStateStr))
        {
            JObject inner = JObject.Parse(gameStateStr);
            outer["game_state"] = inner;
        }

        if (!string.IsNullOrEmpty(sceneName))
        {
            // Save parsed game_state only (not full object)
            SceneTransfer.rawJson = outer["game_state"].ToString(Formatting.None);

            SceneManager.LoadScene(sceneName);
        }
        else
        {
            Debug.LogError("Missing game_name in JSON!");
        }
    }
}
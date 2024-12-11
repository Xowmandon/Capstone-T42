//Author: Benjamin Steinberg
//Date created: 12/10/2024
//Notes: opens red flag racing

using UnityEngine;
using UnityEngine.SceneManagement;

public class StartButton : MonoBehaviour
{
    public void LoadNewScene()
    {
        SceneManager.LoadScene("RedFlagRacing");
    }
}
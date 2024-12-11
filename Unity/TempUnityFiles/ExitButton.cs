using UnityEngine;

public class ExitButton : MonoBehaviour
{
    public GameObject exitButton;
    public void exitGame()
    {
        Application.Unload();
    }
}
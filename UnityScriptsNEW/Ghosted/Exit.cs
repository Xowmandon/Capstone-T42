using UnityEngine;

public class ExitOnClick : MonoBehaviour
{
    private bool canExit = false;

    public void AllowExit(){
        canExit = true;
    }

    void Update(){
        if (canExit && Input.GetMouseButtonDown(0))
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.isPlaying = false;
#else
            Application.Quit();
#endif
        }
    }
}

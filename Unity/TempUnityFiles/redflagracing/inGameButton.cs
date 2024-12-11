//Author: Benjamin Steinberg
//Created: 12/11/2024


using UnityEngine;

public class inGameButton : MonoBehaviour
{
    //private
    private bool doesAgree;
    private rfrgm gameManager;

    public void pressButton()
    {
        gameManager.getAnswer(doesAgree);
    }

    public void SetGameManRef(rfrgm gm)
    {
        gameManager = gm;
    }

    public void setButton(bool input)
    {
        doesAgree = input;
    }
}
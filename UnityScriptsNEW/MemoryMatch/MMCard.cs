//Created by: Benjamin Steinberg
//Date Created: 12/10
//Current State: Fully functional, just need some future UI updates

using UnityEngine;
using UnityEngine.UI;
using TMPro;

public struct Interests
{
    public string[] interests; //grab 4 interests from profile
}

public class MMCard : MonoBehaviour
{
    //Public
    public Button button;
    public TMP_Text buttonText;
    
    //Private
    private GameControllerMM gameCont;

    void Awake()
    {
        hide();
    }
    public void selected()
    {
        if(gameCont.canCheckCards) {
            reveal();
            button.interactable = false;
            button.image.color = new Color(0.863f, 0.824f, 0.784f);
            if(gameCont != null) {
                gameCont.buttonClicked(this);
            }
        }
    }

    public void matched()
    {
        button.image.color = new Color(0.596f, 0.984f, 0.596f);
    }

    public void resetButton()
    {
        button.interactable = true;
        button.image.color = Color.white;
        hide();
    }

    public void reveal()
    {
        buttonText.alpha = 255;
    }

    void hide()
    {
        buttonText.alpha = 0;
    }

    public void SetGameContrRef(GameControllerMM input)
    {
        gameCont = input;
    }
}
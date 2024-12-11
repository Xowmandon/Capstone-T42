//Created by: Benjamin Steinberg
//Date Created: 12/9
//Updates: Fully functional, just need some future UI updates

using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;

public class gridspace : MonoBehaviour
{
    //Public
    public Button button;
    public TMP_Text buttonText;

    //Private
    private GameController gameCont;
    
    void Awake()
    {
        //Debug.Log("debug log working");
    }

    public void SetSpace()
    {
        if(gameCont.playerNum == gameCont.getTurn())
        {
            buttonText.text = gameCont.getText();
            buttonText.color = gameCont.getColor();
            button.interactable = false;
            gameCont.Endturn();
        }
        
        //Debug.Log("SetSpace called");
        //Debug.Log("Player side: " + playerSide);
    }

    public void SetGameContrRef(GameController input)
    {
        gameCont = input;
    }
}
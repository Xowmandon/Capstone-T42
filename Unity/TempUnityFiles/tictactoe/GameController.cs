//Created by: Benjamin Steinberg
//Date Created: 12/9
//Updates: Press T to switch players, need to implement with app and import names, export who won

using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;


public class GameController : MonoBehaviour
{
    //Public
    public TMP_Text[] buttonArr;
    public GameObject gameover;
    public TMP_Text gameoverText;
    public GameObject turnPanel;
    public TMP_Text turnText;
    public int playerNum;
    public string[] playerNames;
    public GameObject exitButton;

    //Private
    private string side;
    private int turnNum;

    void Awake()
    {
        SetGameContrRefonButt();
        side = "X";
        gameover.SetActive(false);
        gameover.SetActive(false);
        exitButton.SetActive(false);
        playerNames[0] = "John";
        playerNames[1] = "Jane";
        playerNum = 0;
        setTurnPanel();
    }

    void Update()
    {
     if (Input.GetKeyDown(KeyCode.T))
        {
            debugSwitchSides();
        }
    }

    void SetGameContrRefonButt()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            buttonArr[i].GetComponentInParent<gridspace>().SetGameContrRef(this);
        }
    }

    public bool getSide()
    {
        return (side == "X");
    }

    public void Endturn()
    {
        if(checkWin()){
            GameOver();
        }
        turnNum++;
        changeSides();
    }

    bool checkWin()
    {
        if (turnNum == 8){
            return true;
        }
        
        // Check rows
        for (int row = 0; row < 3; row++) {
        if (buttonArr[row * 3].text == side && 
            buttonArr[row * 3 + 1].text== side && 
            buttonArr[row * 3 + 2].text == side) 
            {
                return true;
            }
        }

        // Check columns
        for (int col = 0; col < 3; col++) {
            if (buttonArr[col].text == side &&
                buttonArr[col + 3].text == side &&
                buttonArr[col + 2 * 3].text == side) 
                {
                return true;
                }
        }

        // Check diagonals
        if (buttonArr[0].text == side && 
            buttonArr[4].text == side && 
            buttonArr[8].text == side) 
            {
            return true;
            }

        if (buttonArr[2].text == side && 
            buttonArr[4].text == side && 
            buttonArr[6].text == side) 
            {
            return true;
            }
        
        return false;
    }

    void GameOver()
    {
        //deactivate all buttons
        for (int i = 0; i < buttonArr.Length; i++) 
        {
            buttonArr[i].GetComponentInParent<Button>().interactable = false;
        }

        Debug.Log("winner winner chicken dinner");
        
        if (turnNum < 8) 
        {
            gameoverText.text = playerNames[getTurn()] + " Wins!";
            gameoverText.color = getColor();
        }
        else
            gameoverText.text = "It's a tie!";

        turnPanel.SetActive(false);
        gameover.SetActive(true);
        exitButton.SetActive(true);
    }

    void changeSides()
    {
        side = (getSide()) ? "O" : "X";
        setTurnPanel();
    }

    public string getText()
    {
         return side;
    }

    public Color getColor()
    {
        return (getSide()) ? Color.white : Color.blue;
    }

    public int getTurn()
    {
        return turnNum%2;
    }

    void setTurnPanel()
    {
        turnText.text = playerNames[getTurn()] + "'s turn!";
        turnText.color = getColor();
    }

    void debugSwitchSides()
    {
        playerNum = (playerNum == 0) ? 1 : 0;
    }

}
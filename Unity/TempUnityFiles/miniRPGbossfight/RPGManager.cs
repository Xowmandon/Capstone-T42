//Author: Benjamin Steinberg
//Created: 12/11/2024
//Notes: works, need to test out more combat

using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class RPGManager : MonoBehaviour
{
    //Public
    public GameObject[] characters;
    public GameObject enemy;
    public int playerNum = 0;
    public string[] playerNames;
    public GameObject gameoverPanel;
    public TMP_Text gameoverText;
    public TMP_Text gamePanel;
    public int playerTurn = 0;
    public Button[] actionButtons;
    public TMP_Text playerTurnText;

    //Private
    private rpgcharacter[] characterRefs = new rpgcharacter[2];
    private rpgcharacter enemyCharacter;

    void Awake()
    {
        gameoverPanel.SetActive(false);
        getCharRefs();
        setGameManRefChar();
        setGameManRefButtons();
        setPlayerTurnText();

    }
    void Update()
    {
     if (Input.GetKeyDown(KeyCode.T))
        {
            debugSwitchSides();
        }
    }

    void debugSwitchSides()
    {
        playerNum = (playerNum == 0) ? 1 : 0;
    }

    public void receiveAction(moveType type)
    {
        Debug.Log("received action");
        if(playerNum == playerTurn)
        {
            Debug.Log("player turn: " + playerTurn);
            Debug.Log("is dead: " + characterRefs[playerTurn].getIsDead());
            if(!characterRefs[playerTurn].getIsDead())
            {
                Debug.Log("is not dead check");
                switch(type)
                {
                    case moveType.Melee:
                        characterRefs[playerTurn].meleeAttack(enemyCharacter);
                        break;

                    case moveType.Magic:
                        characterRefs[playerTurn].magicAttack(enemyCharacter);
                        break;

                    case moveType.Heal:
                        characterRefs[playerTurn].healAlly(characterRefs[getAlly()]);
                    break;
                }
            }
            playerTurn++;

            if(playerTurn == 2)
            {
            enemyTurn();
            playerTurn = 0;
            }

            setPlayerTurnText();
        }
        

    }

    void enemyTurn()
    {
        enemyCharacter.meleeAttack(characterRefs[0]);
        enemyCharacter.meleeAttack(characterRefs[1]);
    }

    int getAlly()
    {
        if (playerTurn == 0)
        {
            return 1;
        }
        return 0;
    }

    public void gamePanelText(string message)
    {
        string temp;
        if(playerTurn < 2)
        {
            temp = playerNames[playerTurn];
        }
        else
        {
            temp = "Enemy";
        }

        gamePanel.text = temp + message;
    }

    public void gameover(bool allyWin)
    {
        disableButtons();
        gameoverPanel.SetActive(true);
        
        if(allyWin)
        {
            gameoverText.text = "You Win!";
        }
        else
        {
            gameoverText.text = "You Lose:/";
        }
    }

    void enemyWin()
    {
        if(enemyCharacter.getIsDead())
        {
            gameover(true);
        }
    }

    void setGameManRefButtons()
    {
        for(int i = 0; i < 3; i++)
        {
            actionButtons[i].GetComponentInParent<attack>().setGameManager(this);
        }
    }

    void setGameManRefChar()
    {
        characterRefs[0].getGameMan(this);
        characterRefs[1].getGameMan(this);
        enemyCharacter.getGameMan(this);
    }

    void getCharRefs()
    {
        enemyCharacter = enemy.GetComponentInChildren<rpgcharacter>();
        if(enemyCharacter == null)
        {
            Debug.Log("null ref");
        }
        characterRefs[0] = characters[0].GetComponentInChildren<rpgcharacter>();
        characterRefs[1] = characters[1].GetComponentInChildren<rpgcharacter>();
        
    }

    void disableButtons()
    {
        for(int i = 0; i < 3; i++)
        {
            actionButtons[i].interactable = false;
        }
    }

    void setPlayerTurnText()
    {
        playerTurnText.text = "Player Turn: " + playerNames[playerTurn];
    }

    public void deathDispatcher(rpgcharacter victim)
    {
        if(enemyCharacter == victim)
        {
            gameover(true);
        }
        if(characterRefs[0].getIsDead() && characterRefs[1].getIsDead())
        {
            gameover(false);
        }
    }
}
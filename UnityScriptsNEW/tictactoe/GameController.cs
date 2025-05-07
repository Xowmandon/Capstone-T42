//Author: Benjamin Steinberg
//Date Created: 12/9/24

using TMPro;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]
public struct tictactoeData
{
    public string winner;
    public string[] boardState;
    public string nameP1;
    public string nameP2;
    public int lastMoveBy; //initially pass -1
}

public class GameController : MonoBehaviour, IGameStateProvider
{
    public GameObject unityBridgeObj;
    public gridspace[] buttonArr;
    public GameObject gameover;
    public TMP_Text gameoverText;
    public GameObject turnPanel;
    public TMP_Text turnText;
    public string[] playerNames = new string[2];
    public GameObject exitButton;
    public Sprite p1Sprite;
    public Sprite p2Sprite;

    public int myPlayerNum; // 0 or 1
    private int currentTurn => CountFilledTiles() % 2; // Derived
    private string[] boardState = new string[9];
    private string winner = "";
    public bool isLocalPlayerTurn => myPlayerNum == currentTurn && string.IsNullOrEmpty(winner);

    void Start()
    {
        SetRefs();
        gameover.SetActive(false);
        exitButton.SetActive(false);

    
    #if UNITY_EDITOR
        // Inject test data in the editor
        SceneTransfer.rawJson = @"{
    ""winner"": """",
    ""boardState"": [""O"", """", """", """", ""X"", """", """", """", """"],
    ""nameP1"": ""Jenni"",
    ""nameP2"": ""Alex"",
    ""lastMoveBy"": 1
}";

    #endif
    
        if (string.IsNullOrEmpty(SceneTransfer.rawJson))
        {
            Debug.LogWarning("No existing state — starting fresh.");
            boardState = new string[9];
            UpdateBoardUI();
            UpdateTurnPanel();
            return;
        }

        LoadFullGameStateFromJSON(SceneTransfer.rawJson);
    }


    #if UNITY_EDITOR
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.T))
        {
            myPlayerNum = (myPlayerNum == 0) ? 1 : 0;
            Debug.Log($"[DEBUG] Switched to player {myPlayerNum} ({(myPlayerNum == 0 ? "X" : "O")})");
            UpdateTurnPanel();
        }
    }
    #endif


    void SetRefs()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            buttonArr[i].SetGameContrRef(this, i);
        }
    }

    public void OnPlayerClickedSpace(int index)
    {
        if (!isLocalPlayerTurn || !string.IsNullOrEmpty(boardState[index]))
            return;

        boardState[index] = GetSideSymbol(currentTurn);
        UpdateBoardUI();

        if (CheckWin(out string whoWon))
        {
            winner = whoWon;
            gameoverText.text = $"{GetPlayerName(whoWon)} wins!";
            gameover.SetActive(true);
        }

        exitButton.SetActive(true);
        UpdateTurnPanel();
    }

    public string FinalizePlayerMove()
    {
        return GetGameStateJSON();
    }

    public void LoadFullGameStateFromJSON(string json)
    {
        var state = JsonUtility.FromJson<tictactoeData>(json);
        boardState = state.boardState;
        playerNames[0] = state.nameP1;
        playerNames[1] = state.nameP2;
        winner = state.winner;

        myPlayerNum = (state.lastMoveBy == 0) ? 1 : 0;

        UpdateBoardUI();
        UpdateTurnPanel();
    }

    public string GetGameStateJSON()
    {
        tictactoeData state = new tictactoeData
        {
            boardState = boardState,
            nameP1 = playerNames[0],
            nameP2 = playerNames[1],
            winner = winner,
            lastMoveBy = myPlayerNum
        };

        return JsonUtility.ToJson(state);
    }

    void UpdateBoardUI()
    {
        for (int i = 0; i < buttonArr.Length; i++)
        {
            string symbol = boardState[i];
            buttonArr[i].SetDisplay(symbol, GetSprite(symbol));
        }
    }

    void UpdateTurnPanel()
    {
        if (!string.IsNullOrEmpty(winner))
        {
            turnText.text = $"{GetPlayerName(winner)} wins!";
        }
        else if (IsBoardFull())
        {
            turnText.text = "It's a draw!";
        }
        else
        {
            turnText.text = isLocalPlayerTurn
                ? $"Your turn {playerNames[myPlayerNum]}!"
                : $"Waiting for {playerNames[currentTurn]}...";
        }

        turnPanel.SetActive(true);
    }


    int CountFilledTiles()
    {
        int count = 0;
        foreach (var s in boardState)
            if (!string.IsNullOrEmpty(s)) count++;
        return count;
    }

    bool IsBoardFull() => CountFilledTiles() == 9;

    bool CheckWin(out string winnerSymbol)
    {
        string[][] wins = new string[][]
        {
            new[] { boardState[0], boardState[1], boardState[2] },
            new[] { boardState[3], boardState[4], boardState[5] },
            new[] { boardState[6], boardState[7], boardState[8] },
            new[] { boardState[0], boardState[3], boardState[6] },
            new[] { boardState[1], boardState[4], boardState[7] },
            new[] { boardState[2], boardState[5], boardState[8] },
            new[] { boardState[0], boardState[4], boardState[8] },
            new[] { boardState[2], boardState[4], boardState[6] },
        };

        foreach (var line in wins)
        {
            if (!string.IsNullOrEmpty(line[0]) && line[0] == line[1] && line[1] == line[2])
            {
                winnerSymbol = line[0];
                return true;
            }
        }

        winnerSymbol = "";
        return false;
    }

    string GetSideSymbol(int playerIndex) => playerIndex == 0 ? "X" : "O";

    string GetPlayerName(string side) => side == "X" ? playerNames[0] : playerNames[1];

    Sprite GetSprite(string symbol)
    {
        if (symbol == "X") return p1Sprite;
        if (symbol == "O") return p2Sprite;
        return null;
    }
}

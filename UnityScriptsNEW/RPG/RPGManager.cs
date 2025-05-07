//Author: Benjamin Steinberg
//Created on: 12/10/24

using UnityEngine;
using TMPro;
using UnityEngine.UI;
using System;
using System.Collections;
using System.Collections.Generic;

[System.Serializable]
public struct RPGState
{
    public string[] playerNames;
    public string bossId;
    public int playerTurn;
    public int playerNum;
    public moveType lastPlayerMove;
    public float[] playerHPs;
    public StatusType[] playerStatuses;
    public int[] playerStatusDurations;
    public float bossHP;
    public StatusType bossStatus;
    public int bossStatusDuration;
    public int randomSeed;
    public bool playersWon;

    public int myPlayerIndex; // 0 for player 1, 1 for player 2
}

public class RPGManager : MonoBehaviour, IGameStateProvider
{
    private bool allowWaitingPanel = true;
    public rpgcharacter[] characterRefs;
    public enemyAI enemy;
    public int playerNum = 0;
    public GameObject waitingPanel;
    public TMP_Text gameoverText;
    public int playerTurn = 0;
    public Button[] actionButtons;
    public TMP_Text playerTurnText;
    public DialogueManager dialogueManager;
    public Sprite[] statusEffectSprites;
    public moveType prevPlayerMove = moveType.None;

    public int randomSeed = 0;
    public bool playersWon = false;
    private bool gameEnded = false;
    private RPGState lastSyncedState;
    private bool isReplayingPreviousMove = false;
    
    #if UNITY_EDITOR
void Awake()
{
    // Fresh game state for testing from the beginning
    SceneTransfer.rawJson = @"{
        ""playerNames"": [""Jenni"", ""Alex""],
        ""bossId"": ""TheAlgorithm"",
        ""playerTurn"": 0,
        ""playerNum"": 1,
        ""lastPlayerMove"": 0,
        ""playerHPs"": [100.0, 100.0],
        ""playerStatuses"": [""none"", ""none""],
        ""playerStatusDurations"": [0, 0],
        ""bossHP"": 200.0,
        ""bossStatus"": ""none"",
        ""bossStatusDuration"": 0,
        ""randomSeed"": 5678,
        ""playersWon"": false,
        ""myPlayerIndex"": 1
    }";
}
#endif


    void Start()
    {
        LoadFullGameStateFromJSON(SceneTransfer.rawJson);
        waitingPanel.SetActive(false);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.T)) SwitchSides();
    }

    void SwitchSides()
    {
        playerNum = (playerNum == 0) ? 1 : 0;
        UpdateTurnState();
    }

    void UpdateTurnState()
    {
        playerTurnText.text = "Turn: " + characterRefs[playerTurn].charName;

        if (allowWaitingPanel && !isReplayingPreviousMove)
        {
            waitingPanel.SetActive(playerNum != playerTurn);
        }

        updateActionButtons();
    }

    public void receiveAction(moveType type)
    {
        StartCoroutine(receiveActionCoroutine(type));
    }

    private IEnumerator receiveActionCoroutine(moveType type)
    {
        if (characterRefs[playerTurn].getIsDead() || (!isReplayingPreviousMove && playerNum != playerTurn) || characterRefs[playerTurn].madeMove)
            yield break;

        var currentChar = characterRefs[playerTurn];
        currentChar.madeMove = true;
        currentChar.reduceCooldowns();

        // SAVE SNAPSHOT BEFORE ACTION IS TAKEN
        if (!isReplayingPreviousMove)
        {
            SaveSnapshot(); // Save current pre-move state
        }

        // Handle pre-action effects
        bool blocked = false;
        yield return StartCoroutine(currentChar.PreActionStatusCheckCoroutine(() => blocked = true));

        if (blocked || type == moveType.None)
        {
            StartCoroutine(HandlePostDialogueActionsCoroutine());
            yield break;
        }

        string message = type switch
        {
            moveType.Melee => $"{currentChar.charName} attacks with a basic attack!",
            moveType.Magic => $"{currentChar.charName} casts a dazzling spell!",
            moveType.Heal => $"{currentChar.charName} heals their ally!",
            moveType.Ultimate => $"{currentChar.charName} unleashes their ultimate move!",
            _ => ""
        };

        IEnumerator moveCoroutine = ExecuteMoveAndStatus(type, currentChar, () => StartCoroutine(HandlePostDialogueActionsCoroutine()));
        prevPlayerMove = type;

        dialogueManager.EnqueueDialogue(new DialogueEntry(message, () => StartCoroutine(moveCoroutine)));

        Debug.Log($"[RECEIVE] Turn: {playerTurn}, PlayerNum: {playerNum}, IsReplay: {isReplayingPreviousMove}, MadeMove: {characterRefs[playerTurn].madeMove}");
    }

    private IEnumerator ExecuteMoveAndStatus(moveType type, rpgcharacter currentChar, Action onComplete)
    {
        switch (type)
        {
            case moveType.Melee:
                currentChar.meleeAttack(enemy);
                break;
            case moveType.Magic:
                currentChar.magicAttack(enemy);
                break;
            case moveType.Heal:
                currentChar.healAlly(characterRefs[getAlly()]);
                break;
            case moveType.Ultimate:
                currentChar.ultimateAttack(enemy);
                break;
        }

        // Wait until any immediate dialogue finishes
        yield return new WaitUntil(() => dialogueManager.IsQueueEmpty());

        // Handle delayed status effect resolution
        yield return StartCoroutine(currentChar.PostActionStatusCheckCoroutine());

        // Save state after move
        SaveSnapshot();

        // Reset the replay flag here
        isReplayingPreviousMove = false;

        // Continue turn flow
        onComplete?.Invoke();
    }


    private IEnumerator HandlePostDialogueActionsCoroutine()
    {
        // Check if enemy died from player's action or status
        if (enemy.getIsDead())
        {
            if (!gameEnded)
            {
                gameEnded = true;
                dialogueManager.ClearQueue();
                deathDispatcher(enemy);
            }
            yield break;
        }

        // Advance player turn
        playerTurn++;

        // If both players have moved, it's boss's turn
        if (playerTurn >= 2)
        {
            playerTurn = 0;
            characterRefs[0].madeMove = false;
            characterRefs[1].madeMove = false;

            // Check player deaths from status before boss moves
            if (characterRefs[0].getIsDead())
            {
                if (!gameEnded)
                {
                    gameEnded = true;
                    deathDispatcher(characterRefs[0]);
                }
                yield break;
            }
            if (characterRefs[1].getIsDead())
            {
                if (!gameEnded)
                {
                    gameEnded = true;
                    deathDispatcher(characterRefs[1]);
                }
                yield break;
            }

            // Boss's turn
            if (randomSeed == 0)
                randomSeed = UnityEngine.Random.Range(0, 10000);

            randomSeed = enemy.GetNextSeed();

            playerTurnText.text = "Turn: " + enemy.charName;
            rpgcharacter target;
            BossActionType action = enemy.DecideBossAction(out target);

            // Execute boss move, then wait for dialogue and update turn
            enemy.ExecuteBossAction(action, target, () =>
            {
                StartCoroutine(WaitForDialogueThen(() =>
                {
                    UpdateTurnState();
                }));
            });

            yield break;
        }

        // If next player is dead, skip them
        if (characterRefs[playerTurn].getIsDead())
        {
            yield return StartCoroutine(HandlePostDialogueActionsCoroutine());
            yield break;
        }

        yield return new WaitUntil(() => dialogueManager.IsQueueEmpty());
        UpdateTurnState();
    }

    void SaveSnapshot()
    {
        lastSyncedState = new RPGState
        {
            playerNames = new string[]
            {
                characterRefs[0].charName,
                characterRefs[1].charName
            },
            bossId = enemy.GetBossId(),
            playerTurn = playerTurn,
            playerNum = playerNum,
            lastPlayerMove = prevPlayerMove,
            playerHPs = new float[]
            {
                characterRefs[0].health,
                characterRefs[1].health
            },
            playerStatuses = new StatusType[]
            {
                characterRefs[0].currentStatus,
                characterRefs[1].getStatusEffect()
            },
            playerStatusDurations = new int[]
            {
                characterRefs[0].getStatusDuration(),
                characterRefs[1].getStatusDuration()
            },
            bossHP = enemy.health,
            bossStatus = enemy.getStatusEffect(),
            bossStatusDuration = enemy.getStatusDuration(),
            randomSeed = randomSeed,
            playersWon = playersWon,
            myPlayerIndex = playerNum
        };
    }

    private IEnumerator WaitForDialogueThen(Action callback)
    {
        yield return new WaitUntil(() => dialogueManager.IsQueueEmpty());
        callback?.Invoke();
    }

    int getAlly() => (playerTurn == 0) ? 1 : 0;

    public void gameover(bool allyWin)
    {
        disableButtons();
        playersWon = allyWin;

        waitingPanel.SetActive(true);
        gameoverText.text = allyWin ? "You Win!" : "You Lose:/";
    }

    void setGameManRefButtons()
    {
        foreach (var button in actionButtons)
            button.GetComponentInParent<attack>().setGameManager(this);
    }

    void setGameManRefChar()
    {
        characterRefs[0].getGameMan(this);
        characterRefs[1].getGameMan(this);
        enemy.getGameMan(this);
    }

    void disableButtons()
    {
        foreach (var button in actionButtons)
            button.interactable = false;
    }

    public void deathDispatcher(rpgcharacter victim)
    {
        if (gameEnded) return;
        gameEnded = true;
        string deathMessage = $"{victim.charName} has died!";
        dialogueManager.EnqueueDialogue(new DialogueEntry(deathMessage, null, () =>
        {
            if (enemy == victim)
            {
                string deathLine = enemy.GetDeathLine();
                if (!string.IsNullOrEmpty(deathLine))
                {
                    dialogueManager.EnqueueDialogue(new DialogueEntry(deathLine, null, () =>
                    {
                        gameover(true);
                    }));
                }
                else
                {
                    gameover(true);
                }
            }
            else if (characterRefs[0].getIsDead() && characterRefs[1].getIsDead())
            {
                gameover(false);
            }
        }));
    }

    void updateActionButtons()
    {
        foreach (var button in actionButtons)
        {
            attack atk = button.GetComponent<attack>();
            atk.setCharacter(characterRefs[playerTurn]);
            atk.refreshButton();
        }
    }

    void updateNames()
    {
        if (characterRefs[0]?.displayName != null)
            characterRefs[0].displayName.text = characterRefs[0].charName;

        if (characterRefs[1]?.displayName != null)
            characterRefs[1].displayName.text = characterRefs[1].charName;


        if (enemy != null && enemy.displayName != null)
        {
            if (string.IsNullOrEmpty(enemy.charName))
            {
                Debug.LogWarning("enemy.charName is null or empty in updateNames().");
                enemy.charName = "Unknown";
            }

            try
            {
                enemy.displayName.text = enemy.charName;

                var rt = enemy.displayName.GetComponent<RectTransform>();
                if (rt != null && (float.IsNaN(rt.localScale.x) || float.IsInfinity(rt.localScale.x)))
                {
                    Debug.LogError("displayName RectTransform has invalid scale!");
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"Exception while setting enemy display name: {e}");
            }
        }
        else
        {
            Debug.LogWarning("enemy or enemy.displayName was null in updateNames().");
        }
    }

    public string GetGameStateJSON()
    {
        return JsonUtility.ToJson(lastSyncedState);
    }

    public void LoadFullGameStateFromJSON(string json)
    {
        setGameManRefChar();
        setGameManRefButtons();

        RPGState state = default;
        bool isFirstTurn = false;

        if (string.IsNullOrWhiteSpace(json) || json.Trim() == "{}")
        {
            Debug.Log("[Load] Empty or null JSON — initializing fresh game.");
            isFirstTurn = true;
        }
        else
        {
            state = JsonUtility.FromJson<RPGState>(json);
            isFirstTurn = (state.lastPlayerMove == moveType.None);
        }

        // Random seed and identity toggle
        randomSeed = isFirstTurn ? UnityEngine.Random.Range(0, 10000) : state.randomSeed;
        UnityEngine.Random.InitState(randomSeed);

        playersWon = false;
        playerNum = isFirstTurn ? 0 : (state.myPlayerIndex == 0 ? 1 : 0);

        // Initialize characters
        for (int i = 0; i < characterRefs.Length; i++)
        {
            characterRefs[i].health = characterRefs[i].MaxHealth;
            characterRefs[i].madeMove = false;

            // Always use name from JSON
            string incomingName = state.playerNames != null && i < state.playerNames.Length ? state.playerNames[i] : $"Player {i + 1}";
            characterRefs[i].SetName(incomingName);

            if (!isFirstTurn)
            {
                characterRefs[i].applyStatus(state.playerStatuses[i], state.playerStatusDurations[i]);
                characterRefs[i].health = state.playerHPs[i];
            }

            characterRefs[i].updateHealthbar();
        }

        // Initialize enemy
        enemy.SetSeed(randomSeed);
        if (isFirstTurn)
        {
            enemy.AssignRandomBoss();
            enemy.AssignSelectedBoss(applyDefaultHealth: true);
        }
        else
        {
            enemy.AssignBossById(state.bossId);
            enemy.health = state.bossHP;
            enemy.applyStatus(state.bossStatus, state.bossStatusDuration);
        }

        enemy.updateHealthbar();

        updateNames();
        updateActionButtons();

        if (isFirstTurn)
        {
            playerTurn = 0;
            isReplayingPreviousMove = false;
            allowWaitingPanel = true;

            dialogueManager.EnqueueDialogue(new DialogueEntry("Defeat the boss!", null, () =>
            {
                dialogueManager.EnqueueDialogue(new DialogueEntry(enemy.GetOpeningLine(), null, () =>
                {
                    UpdateTurnState();
                }));
            }));

            return;
        }

        // Replay last move if mid-game
        isReplayingPreviousMove = true;
        allowWaitingPanel = false;

        dialogueManager.EnqueueDialogue(new DialogueEntry("Resuming battle — replaying last moves...", null, () =>
        {
            playerTurn = (playerNum == 0) ? 1 : 0;
            receiveAction(state.lastPlayerMove);
            StartCoroutine(EnableWaitingPanelAfterDialogue());
        }));
    }


    private IEnumerator EnableWaitingPanelAfterDialogue()
    {
        yield return new WaitUntil(() => dialogueManager.IsQueueEmpty());
        allowWaitingPanel = true;
        UpdateTurnState(); 
    }
}
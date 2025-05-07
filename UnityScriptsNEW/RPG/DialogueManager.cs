//Author: Benjamin Steinberg
//Created on: 4/5/2025

using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

[System.Serializable]
public class DialogueEntry
{
    public string dialogue;
    public Action action;
    public Action postActionCallback;

    public DialogueEntry(string dialogue, Action action = null, Action postActionCallback = null)
    {
        this.dialogue = dialogue;
        this.action = action;
        this.postActionCallback = postActionCallback;
    }
}

public class DialogueManager : MonoBehaviour
{
    public TMP_Text dialogueText;
    public float typingSpeed = 0.05f;
    public float postTextLinger = 0.5f;
    public float postActionLinger = 1.0f;

    private Coroutine currentDialogue;
    private Queue<DialogueEntry> dialogueQueue = new Queue<DialogueEntry>();

    public void EnqueueDialogue(DialogueEntry entry)
    {
        dialogueQueue.Enqueue(entry);

        if (currentDialogue == null)
        {
            ProcessQueue();
        }
    }

    private void ProcessQueue()
    {
        if (dialogueQueue.Count > 0)
        {
            DialogueEntry entry = dialogueQueue.Dequeue();
            currentDialogue = StartCoroutine(RunDialogueEntry(entry));
        }
    }

    private IEnumerator RunDialogueEntry(DialogueEntry entry)
    {
        ClearDialogue();

        string dialogueToDisplay = entry.dialogue ?? "";

        foreach (char letter in dialogueToDisplay)
        {
            dialogueText.text += letter;
            yield return new WaitForSeconds(typingSpeed);
        }

        yield return new WaitForSeconds(postTextLinger);

        entry.action?.Invoke();
        yield return new WaitForSeconds(postActionLinger);

        entry.postActionCallback?.Invoke();

        currentDialogue = null;
        ProcessQueue();
    }

    private void ClearDialogue()
    {
        dialogueText.text = "";
    }

    public bool IsQueueEmpty()
    {
        return dialogueQueue.Count == 0 && currentDialogue == null;
    }

    public void ClearQueue()
    {
        dialogueQueue.Clear();
    }
}
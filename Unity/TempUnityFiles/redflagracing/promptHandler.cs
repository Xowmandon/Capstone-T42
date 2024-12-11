//Author: Benjamin Steinberg
//Created: 12/11/2024
//Notes: Need way to import prompts, add more prompts

using System.Collections.Generic;
using UnityEngine;

public class promptHandler : MonoBehaviour
{
    private List<string> availablePrompts;
    private string lastSelectedPrompt = null;

    public promptHandler()
    {
        ResetPrompts();
    }

    public string GetRandomPrompt()
    {
        if (availablePrompts.Count == 0)
        {
            Debug.LogWarning("No more prompts available!");
            return null;
        }

        string selectedPrompt;

        do
        {
            int randomIndex = UnityEngine.Random.Range(0, availablePrompts.Count);
            selectedPrompt = availablePrompts[randomIndex];
        } while (selectedPrompt == lastSelectedPrompt && availablePrompts.Count > 1);

        availablePrompts.Remove(selectedPrompt);
        lastSelectedPrompt = selectedPrompt;

        return selectedPrompt;
    }

    public void ResetPrompts()
    {
        availablePrompts = new List<string>
        {
            "They always open every door",
            "They vote differently than you",
            "Pooring milk before cereal",
            "Going to the dentist twice a year",
            "They dislike cats",
            "Rewatches Friends daily",
            "Going out every weekend",
            "Cheesecake Factory Date?"
        };
        lastSelectedPrompt = null;
    }
}
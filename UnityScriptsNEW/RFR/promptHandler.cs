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
        "They vote differently than you",
        "Rewatches Friends religiously",
        "Only uses 1 pillow and thinks that’s normal",
        "Cheesecake Factory Date?",
        "Says Disneyland is overrated",
        "Thinks astrology is fake",
        "Still talks their ex",
        "Never tips at restaurants",
        "Insists on setting a thermostat war at 68°F year-round",
        "Still follows their ex’s mom on Instagram",
        "Wears socks to bed—by choice",
        "Only listens to true crime media... to fall asleep",
        "Eats string cheese by biting it",
        "Sets 10 alarms but gets up on the 11th",
        "Says their dream wedding is “a courthouse and fast food”"
    };

    }
}
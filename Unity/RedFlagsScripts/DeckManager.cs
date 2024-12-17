using UnityEngine;
using System.Collections.Generic;

public class DeckManager : MonoBehaviour
{
    [SerializeField] 
    private List<GameObject> cards; // Assign your cards in the Inspector

    private int round = 0;
    private const int cardsPerRound = 2;

    void Start()
    {
        // Hide all cards initially
        foreach (GameObject card in cards)
        {
            card.SetActive(false);
        }

        // Start the first round
        StartRound();
    }

    public void StartRound()
    {
        if (round * cardsPerRound >= cards.Count)
        {
            Debug.Log("All rounds complete!");
            return; // No more cards left
        }

        // Activate two cards for the current round
        for (int i = 0; i < cardsPerRound; i++)
        {
            int cardIndex = round * cardsPerRound + i;
            if (cardIndex < cards.Count)
            {
                cards[cardIndex].SetActive(true);
            }
        }

        round++;
    }

    public void EndRound()
    {
        // Hide the current round's cards
        for (int i = 0; i < cardsPerRound; i++)
        {
            int cardIndex = (round - 1) * cardsPerRound + i;
            if (cardIndex < cards.Count)
            {
                cards[cardIndex].SetActive(false);
            }
        }

        // Start the next round
        StartRound();
    }
}


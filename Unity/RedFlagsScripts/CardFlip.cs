using UnityEngine;

[RequireComponent(typeof(BoxCollider2D))]
public class CardFlip : MonoBehaviour
{
    [SerializeField] [Tooltip("Should the card flip when the mouse hovers over it?")]
    private bool flipOnMouseHover = false;
    [SerializeField] [Tooltip("Card shadow has a shadow that should be flipped with the card")]
    private bool useShadow = true;
    [SerializeField] private GameObject cardBack, cardFront;
    [SerializeField] private Transform cardShadow;
    [SerializeField] private float flipDuration = 0.5f;
    [SerializeField] private GameObject redFlagButton; // Button that appears after flip
    private Transform previousSide; // The side of the card currently shown
    private Transform targetSide; // The side of the card currently hidden, to be shown

    private bool flip = false;
    private float elapsedTime = 0;
    private bool isFlipped = false; // Track the flip state

    // Add this line
    public bool IsFlipped { get; private set; } = false;

    private void Start()
    {
        // Ensure the card starts on its back
        if (cardBack != null && cardFront != null)
        {
            cardBack.SetActive(true);
            cardFront.SetActive(false);
            cardBack.transform.localScale = Vector3.one;
            cardFront.transform.localScale = new Vector3(0, 1, 1); // Start invisible
        }

        // Ensure the shadow is correctly initialized
        if (useShadow && cardShadow != null)
        {
            cardShadow.localScale = Vector3.one;
        }

        // Initially hide the red flag button
        if (redFlagButton != null)
        {
            redFlagButton.SetActive(false);
        }
    }

    private void OnMouseEnter()
    {
        if (!flipOnMouseHover) return;
        FlipCard();
    }

    private void OnMouseExit()
    {
        if (!flipOnMouseHover) return;
        FlipCard();
    }

    public void FlipCard()
    {
        if (cardBack == null || cardFront == null) return;

        // Determine the current and target sides
        if (cardBack.activeInHierarchy)
        {
            previousSide = cardBack.transform;
            targetSide = cardFront.transform;
        }
        else
        {
            previousSide = cardFront.transform;
            targetSide = cardBack.transform;
        }

        flip = true;
        elapsedTime = 0; // Reset flip timing

        // Update the IsFlipped status
        IsFlipped = !IsFlipped;
    }

    private void Update()
    {
        if (!flip) return;

        elapsedTime += Time.deltaTime;
        float t = elapsedTime / flipDuration;
        t = t * t * (3f - 2f * t); // Smoothstep interpolation

        // First half of the flip
        if (previousSide != null && previousSide.gameObject.activeInHierarchy)
        {
            previousSide.localScale = new Vector3(Mathf.Lerp(1, 0, t), 1, 1);
            if (useShadow && cardShadow != null)
                cardShadow.localScale = new Vector3(Mathf.Lerp(1, 0, t), 1, 1);

            if (elapsedTime >= flipDuration)
            {
                previousSide.gameObject.SetActive(false);
                targetSide.gameObject.SetActive(true);
                elapsedTime = 0;

                // Once the card has flipped, enable the red flag button
                if (redFlagButton != null)
                {
                    redFlagButton.SetActive(true);
                }
            }
        }
        // Second half of the flip
        else if (targetSide != null && targetSide.gameObject.activeInHierarchy)
        {
            targetSide.localScale = new Vector3(Mathf.Lerp(0, 1, t), 1, 1);
            if (useShadow && cardShadow != null)
                cardShadow.localScale = new Vector3(Mathf.Lerp(0, 1, t), 1, 1);

            if (elapsedTime >= flipDuration)
            {
                flip = false; // Flip complete
                elapsedTime = 0;
            }
        }
    }
}



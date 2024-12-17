using UnityEngine;

public class CardFlipManager : MonoBehaviour
{
    private Camera cam;
    [SerializeField] [Tooltip("Create a layer and assign it to this field and the objects you want to be able to grab")] 
    private LayerMask CardMask;

    private GameObject CardHit;
    private Vector3 mousePos;

    void Start()
    {
        cam = Camera.main;
    }

    //cast to detect if the mouse is on a card
    private void CardCast()
    {
        mousePos = cam.ScreenToWorldPoint(Input.mousePosition);

        Collider2D hit = Physics2D.OverlapPoint(mousePos, CardMask);
        if(hit != null) CardHit = hit.gameObject;
        else CardHit = null;
    }

    void Update()
    {
        if(Input.GetMouseButtonDown(1)) CardCast();

        if(CardHit != null)
        {
            if(CardHit.TryGetComponent<CardFlip>(out CardFlip cardFlip)) cardFlip.FlipCard();
            CardHit = null;
        }
    }
}


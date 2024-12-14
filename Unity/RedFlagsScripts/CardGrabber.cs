using UnityEngine;

public class CardGrabber : MonoBehaviour
{
    //singleton
    public static CardGrabber Instance { get; private set; }
    private void Awake()
    {
        if(Instance != null && Instance != this) Destroy(this); 
        else Instance = this;
    }

    private Camera cam;
    [SerializeField] [Tooltip("Create a layer and assign it to this field and the objects you want to be able to grab")] 
    private LayerMask CardMask;

    [Header("Settings")]
    [SerializeField] private float DragSpeed = 30f;
    [SerializeField] private float CardHoverRotationSpeed = 60f;
    [SerializeField] private float CardMovementRotationStrength = 270f;
    [SerializeField] private bool ResetPositionOnRealease = true;

    private GameObject CardHit;

    private bool isDragging = false;

    private Vector3 rotOffset;
    private float tiltX;
    private float tiltY;
    private Vector3 mousePos;
    Vector3 currentDirection;
    Vector3 previousPosition;
    Vector3 currentPosition;
    Vector3 DragStartPosition;

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
        else if(!isDragging)
        {
            CardHit = null;
        }    
    }

    void Update()
    {
        if(CardHit == null || !isDragging) CardCast();

        if(CardHit != null)
        {
            if(ResetPositionOnRealease && Input.GetMouseButtonDown(0)) DragStartPosition = CardHit.transform.position;
            if(Input.GetMouseButton(0))
            {
                previousPosition = CardHit.transform.position;
                isDragging = true;
                DragCard();
            }
            else
            {
                isDragging = false;
                CardHoverRotation();
            }
            
            if(Input.GetMouseButtonUp(0)) CardDrop();
        }
    }

    private void DragCard()
    {
        if(CardHit == null) return;
        Vector3 pos = cam.ScreenToWorldPoint(Input.mousePosition);
        pos.z = 0f;
        CardHit.transform.position = 
            Vector3.Lerp(
                CardHit.transform.position, pos, Time.deltaTime * DragSpeed);//move the card with delay

        //controls the card visuals depth position
        CardHit.transform.GetChild(0).position = new Vector3(
            CardHit.transform.GetChild(0).position.x, CardHit.transform.GetChild(0).position.y, -.5f);

        MovementRotation();
    }

    private void MovementRotation()
    {
        //rotate the card visuals relative to the card object movement
        currentPosition = CardHit.transform.position;
        currentDirection = currentPosition-previousPosition;
        previousPosition = currentPosition;
        
        CardHit.transform.GetChild(0).localEulerAngles = new(0, 0, currentDirection.x * -CardMovementRotationStrength);
    }

    private void CardDrop()
    {
        isDragging = false;
        if(CardHit == null) return;
        if(ResetPositionOnRealease)
        {
            StartCoroutine(Lerpers.LerpTransform(CardHit.transform, DragStartPosition, Lerpers.OutQuad(.05f)));
        }
        else
        {
            Vector3 pos = CardHit.transform.position;
            pos.z = 0f;
            CardHit.transform.position = pos;
        }
        CardHit.transform.GetChild(0).eulerAngles = new(0, 0, 0);//reset the card visuals rotation
        CardHit.transform.GetChild(0).position = new Vector3(CardHit.transform.GetChild(0).position.x,
             CardHit.transform.GetChild(0).position.y, 0f);
    }

    //rotate the card visuals relative to the cursor position on the card
    private void CardHoverRotation()
    {
        rotOffset = CardHit.transform.position - mousePos;
        tiltX = rotOffset.y *-1;
        tiltY = rotOffset.x;
        CardHit.transform.GetChild(0).eulerAngles = new(tiltX * CardHoverRotationSpeed, tiltY * CardHoverRotationSpeed, 0);
    }
}
using UnityEngine;
using UnityEngine.EventSystems;

public class Ghost : MonoBehaviour, IPointerClickHandler
{
    private Vector2 direction;
    public float speed;
    public float minSpeed = 12f;
    public float maxSpeed = 18f;
    private Camera cam;
    private bool clickedFlag = true;

    void Start()
    {
        cam = Camera.main;
        direction = Random.insideUnitCircle.normalized;
        speed = Random.Range(minSpeed, maxSpeed);
    }

    void Update()
    {
        transform.Translate(direction * speed * Time.deltaTime);

        Vector2 min = cam.ViewportToWorldPoint(new Vector2(0, 0));
        Vector2 max = cam.ViewportToWorldPoint(new Vector2(1, 1));
        Vector2 pos = transform.position;

        if (pos.x <= min.x || pos.x >= max.x)
        {
            direction.x *= -1;
            pos.x = Mathf.Clamp(pos.x, min.x, max.x);
        }

        if (pos.y <= min.y || pos.y >= max.y)
        {
            direction.y *= -1;
            pos.y = Mathf.Clamp(pos.y, min.y, max.y);
        }

        transform.position = pos;
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        if (clickedFlag){
            clickedFlag = false;
            speed = 0;
            GH_GameManager.instance.GhostTapped(transform.position, gameObject);
        }
        
    }
}

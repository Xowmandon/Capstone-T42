//Author: Allison Tang

using UnityEngine;

public class GhostDrifter : MonoBehaviour
{
    public GhostGameManager gameManager;
    private RectTransform rectTransform;
    private Vector2 velocity;

    public float speed = 50f;

    private float areaWidth = 400f;
    private float areaHeight = 600f;

    void Start(){
        rectTransform = GetComponent<RectTransform>();

        //random direction
        velocity = Random.insideUnitCircle.normalized * speed;
    }

    void Update(){
    if(gameManager != null && gameManager.IsGameOver())
        return;

    rectTransform.anchoredPosition += velocity * Time.deltaTime;

    Vector2 pos = rectTransform.anchoredPosition;

    if(Mathf.Abs(pos.x) > areaWidth){
        pos.x = Mathf.Sign(pos.x) * areaWidth;
        velocity.x *= -1;
    }

    if(Mathf.Abs(pos.y) > areaHeight){
        pos.y = Mathf.Sign(pos.y) * areaHeight;
        velocity.y *= -1;
    }

    rectTransform.anchoredPosition = pos;
    }

}

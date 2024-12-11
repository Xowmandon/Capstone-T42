using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasketController : MonoBehaviour
{
    public float moveSpeed = 5f; // Speed at which the basket moves
    private float targetX; // The target position for the basket

    void Start()
    {
        transform.position = new Vector3(750, transform.position.y, transform.position.z);
        targetX = transform.position.x;
    }

    void Update()
    {
        MoveBasket();
    }

    void MoveBasket()
    {
        // Check for touch input
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            targetX = touch.position.x;
        }
        // Check for mouse input (for testing in the Unity editor)
        else if (Input.GetMouseButton(0))
        {
            targetX = Input.mousePosition.x;
        }

        // Convert screen position to world position
        Vector3 screenPos = Camera.main.ScreenToWorldPoint(new Vector3(targetX, 0f, Camera.main.nearClipPlane)); // Use nearClipPlane for z

        // Keep the y position constant to only move horizontally
        screenPos.y = transform.position.y;

        // Move the basket smoothly towards the target position
        transform.position = Vector3.Lerp(transform.position, screenPos, moveSpeed * Time.deltaTime);
    }
}
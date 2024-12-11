using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CloudMover : MonoBehaviour
{
    public float speed = 2f; // Speed of the cloud's movement
    public float resetPosition = 10f; // Position where the cloud resets
    public float startPosition = -10f; // Position where the cloud starts
    public float buffer = 0.5f;
    //public bool gameStarted = false;

void Start()
{
    Camera mainCamera = Camera.main;

    // Calculate the horizontal edges of the camera view
    float screenHalfWidth = mainCamera.orthographicSize * mainCamera.aspect;

    // Set start and reset positions relative to the camera
    startPosition = -screenHalfWidth - buffer; // Left off-screen
    resetPosition = screenHalfWidth + buffer; // Right off-screen
}
    void Update()
    {
            // Move the cloud along its local x-axis
            transform.Translate(Vector3.right * speed * Time.deltaTime, Space.World);

            // Check if the cloud has gone beyond the reset position
            if (transform.position.x > resetPosition)
            {
                // Reset the cloud's position to the start
                transform.position = new Vector3(startPosition, transform.position.y, transform.position.z);
            }
    }
}
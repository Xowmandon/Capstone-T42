using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HearFalling : MonoBehaviour
{
    public float fallSpeed = 5f;
    public int points; // Assign points to the heart
    private float screenWidth;

    void Start()
    {
        screenWidth = Camera.main.orthographicSize * Camera.main.aspect; // For 2D games
    }

    void Update()
    {
        transform.Translate(Vector3.down * fallSpeed * Time.deltaTime);
        
        if (transform.position.y < -5) // Adjust the y-value as per your scene
        {
            Destroy(gameObject); // Destroy heart when it goes off screen
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if(collision.gameObject.CompareTag("Basket"))
        {
            FindObjectOfType<ScoreManager>().AddScore(points);
            Destroy(gameObject); // Destroy heart after scoring
        }
        
    }

    public static void SpawnHeart(GameObject heartPrefab)
    {
        float spawnX = Random.Range(-5f, 5f); // Adjust range
        Vector3 spawnPosition = new Vector3(spawnX, 5f, 0f); // Adjust y-value
        Instantiate(heartPrefab, spawnPosition, Quaternion.identity);
    }
}

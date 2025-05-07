//Author: Allison Tang

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeartSpawner : MonoBehaviour
{
    public GameObject[] heartPrefabs; // Array to store heart prefabs
    public float spawnInterval = 1f; // Time between spawns
    private GameObject[] clouds;     // Array to store cloud objects
    private bool gameStarted = false;
    private bool gameOver = false;

    void Start()
    {
        // Find all clouds in the scene
        clouds = GameObject.FindGameObjectsWithTag("Cloud");
    }

    void Update()
    {
        if(gameStarted && !IsInvoking("SpawnHeart"))
        {
            InvokeRepeating("SpawnHeart", 0f, spawnInterval);
        }

        if (gameOver)
        {
            CancelInvoke("SpawnHeart"); // Stop spawning hearts
        }
    }

    void SpawnHeart()
    {
       if (clouds.Length == 0) return; // Exit if no clouds are found

    // Randomly select a cloud
    int randomCloudIndex = Random.Range(0, clouds.Length);
    GameObject selectedCloud = clouds[randomCloudIndex];

    // Get all spawn points (child objects) of the selected cloud
    Transform[] spawnPoints = selectedCloud.GetComponentsInChildren<Transform>();

    // Exclude the cloud's own transform and pick a child spawn point
    List<Transform> validSpawnPoints = new List<Transform>();
    foreach (Transform point in spawnPoints)
    {
        if (point != selectedCloud.transform)
            validSpawnPoints.Add(point);
    }

    if (validSpawnPoints.Count == 0) return; // Exit if no spawn points are found

    Transform randomSpawnPoint = validSpawnPoints[Random.Range(0, validSpawnPoints.Count)];

    // Randomly select a heart prefab
    int randomHeartIndex = Random.Range(0, heartPrefabs.Length);
    GameObject heartToSpawn = heartPrefabs[randomHeartIndex];

    // Instantiate the heart at the chosen spawn point
    Instantiate(heartToSpawn, randomSpawnPoint.position, Quaternion.identity);
    }

    public void StartGame()
    {
        gameStarted = true;
    }

    public void EndGame()
    {
        gameOver = true; 
        CancelInvoke("SpawnHeart"); // Stop repeating the spawn function
        Debug.Log("Heart Spawner stopped!");
    }
}

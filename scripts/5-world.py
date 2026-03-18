import os
def create_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name: os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(content)

java_path = "app/src/main/java/com/genesis/pokemon"

create_file(f"{java_path}/WorldEngine.java", """package com.genesis.pokemon;
import android.graphics.RectF;

public class WorldEngine {
    // A simple Warp point: if player enters this Rect, move to new Map
    public static class WarpPoint {
        public RectF zone;
        public String targetMap;
        public float spawnX, spawnY;

        public WarpPoint(float x, float y, float w, float h, String target, float sx, float sy) {
            zone = new RectF(x, y, x + w, y + h);
            targetMap = target;
            spawnX = sx;
            spawnY = sy;
        }
    }
    
    // Check if player triggered a house entrance
    public static WarpPoint checkWarps(float px, float py) {
        // Example: House in Littleroot at 800, 200
        WarpPoint littlerootHouse = new WarpPoint(800, 200, 100, 100, "HOUSE_INT", 400, 700);
        if (littlerootHouse.zone.contains(px, py)) return littlerootHouse;
        return null;
    }
}""")

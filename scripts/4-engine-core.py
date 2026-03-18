import os

print("Generating 2D Game Engine Core...")
JAVA_PKG_DIR = "app/src/main/java/com/genesis/pokemon"
os.makedirs(JAVA_PKG_DIR, exist_ok=True)

# 1. THE GAME THREAD (The Heartbeat)
game_thread_java = """package com.genesis.pokemon;

import android.graphics.Canvas;
import android.view.SurfaceHolder;

public class GameThread extends Thread {
    private SurfaceHolder surfaceHolder;
    private GameView gameView;
    private boolean running;

    public GameThread(SurfaceHolder surfaceHolder, GameView gameView) {
        this.surfaceHolder = surfaceHolder;
        this.gameView = gameView;
    }

    public void setRunning(boolean isRunning) { running = isRunning; }

    @Override
    public void run() {
        while (running) {
            Canvas canvas = null;
            try {
                canvas = surfaceHolder.lockCanvas();
                synchronized (surfaceHolder) {
                    gameView.update(); // Calculate physics & movement
                    gameView.draw(canvas); // Render the graphics
                }
            } catch (Exception e) { e.printStackTrace(); }
            finally {
                if (canvas != null) {
                    try { surfaceHolder.unlockCanvasAndPost(canvas); }
                    catch (Exception e) { e.printStackTrace(); }
                }
            }
        }
    }
}
"""
with open(f"{JAVA_PKG_DIR}/GameThread.java", "w", encoding="utf-8") as f:
    f.write(game_thread_java)

# 2. THE GAME VIEW (Rendering, Trailing Pokemon, and Grass)
game_view_java = """package com.genesis.pokemon;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class GameView extends SurfaceView implements SurfaceHolder.Callback {
    private GameThread thread;
    private Paint paint;
    
    // Player Physics
    public float playerX = 500f, playerY = 500f;
    public float speed = 10f;
    public boolean movingUp, movingDown, movingLeft, movingRight;

    // Trailing Pokemon Physics
    public float followerX = 500f, followerY = 550f;

    public GameView(Context context, AttributeSet attrs) {
        super(context, attrs);
        getHolder().addCallback(this);
        thread = new GameThread(getHolder(), this);
        setFocusable(true);
        paint = new Paint();
    }

    // --- GAME LOGIC (Physics, Following, Interactions) ---
    public void update() {
        // 1. Move Player
        if (movingUp) playerY -= speed;
        if (movingDown) playerY += speed;
        if (movingLeft) playerX -= speed;
        if (movingRight) playerX += speed;

        // 2. Trailing Pokemon Logic (Lerp - Linear Interpolation)
        // The Pokemon smoothly glides towards the player's previous position
        float dx = playerX - followerX;
        float dy = playerY - followerY;
        float distance = (float) Math.sqrt(dx * dx + dy * dy);
        
        // Only move if the Pokemon is more than 60 pixels away (trailing distance)
        if (distance > 60) {
            followerX += dx * 0.1f;
            followerY += dy * 0.1f;
        }

        // 3. Grass Rustling Logic (Placeholder)
        // if (TileMap.isGrass(playerX, playerY)) { triggerAnimation("rustle"); checkWildEncounter(); }
    }

    // --- RENDERING (Drawing the world) ---
    @Override
    public void draw(Canvas canvas) {
        super.draw(canvas);
        if (canvas != null) {
            // Draw Background (Hoenn Grass)
            canvas.drawColor(Color.parseColor("#4CAF50")); 

            // Draw Trailing Pokemon (Red Box for now)
            paint.setColor(Color.RED);
            canvas.drawRect(followerX - 25, followerY - 25, followerX + 25, followerY + 25, paint);

            // Draw Player (Blue Box for now)
            paint.setColor(Color.BLUE);
            canvas.drawRect(playerX - 30, playerY - 30, playerX + 30, playerY + 30, paint);
            
            // Draw Trees/Houses would go here by looping through a TileMap array
        }
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        thread.setRunning(true);
        thread.start();
    }

    @Override public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {}
    
    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        boolean retry = true;
        while (retry) {
            try { thread.setRunning(false); thread.join(); retry = false; } 
            catch (InterruptedException e) { e.printStackTrace(); }
        }
    }
}
"""
with open(f"{JAVA_PKG_DIR}/GameView.java", "w", encoding="utf-8") as f:
    f.write(game_view_java)

# 3. WIRING UP THE CONTROLS IN MAIN ACTIVITY
main_activity_java = """package com.genesis.pokemon;

import android.app.Activity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {
    private GameView gameView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gameView = findViewById(R.id.game_viewport);

        // Map D-Pad Buttons to Game Physics
        setupButton(R.id.btn_up, "UP");
        setupButton(R.id.btn_down, "DOWN");
        setupButton(R.id.btn_left, "LEFT");
        setupButton(R.id.btn_right, "RIGHT");
    }

    private void setupButton(int id, final String direction) {
        Button btn = findViewById(id);
        btn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                boolean isPressed = (event.getAction() == MotionEvent.ACTION_DOWN || event.getAction() == MotionEvent.ACTION_MOVE);
                
                if (direction.equals("UP")) gameView.movingUp = isPressed;
                if (direction.equals("DOWN")) gameView.movingDown = isPressed;
                if (direction.equals("LEFT")) gameView.movingLeft = isPressed;
                if (direction.equals("RIGHT")) gameView.movingRight = isPressed;
                
                return true;
            }
        });
    }
}
"""
with open(f"{JAVA_PKG_DIR}/MainActivity.java", "w", encoding="utf-8") as f:
    f.write(main_activity_java)

print("Engine Core Generated.")

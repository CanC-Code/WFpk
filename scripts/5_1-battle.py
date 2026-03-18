name: Genesis 6.0 - RPG Core Engine

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-engine:
    runs-on: ubuntu-latest
    steps:
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Install Dependencies
        run: pip install Pillow requests

      - name: Initialize Workspace
        run: mkdir -p MyPokemonGame/scripts

      - name: Generate Genesis Scripts
        run: |
          cd MyPokemonGame
          
          # --- SCRIPT 1: STABLE SCAFFOLD ---
          cat << 'EOF' > scripts/1-scaffold.py
          import os
          def create_file(path, content):
              dir_name = os.path.dirname(path)
              if dir_name: os.makedirs(dir_name, exist_ok=True)
              with open(path, 'w', encoding='utf-8') as f: f.write(content)

          create_file("build.gradle", "plugins { id 'com.android.application' version '8.4.0' apply false }")
          create_file("settings.gradle", "pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }; dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }; include ':app'")
          create_file("gradle.properties", "android.useAndroidX=true\nandroid.enableJetifier=true")
          create_file("app/build.gradle", "plugins { id 'com.android.application' }; android { namespace 'com.genesis.pokemon'; compileSdk 34; defaultConfig { applicationId 'com.genesis.pokemon'; minSdk 24; targetSdk 34; versionCode 1; versionName '1.6' }; buildTypes { release { minifyEnabled false } }; compileOptions { sourceCompatibility JavaVersion.VERSION_17; targetCompatibility JavaVersion.VERSION_17 } }; dependencies { implementation 'androidx.appcompat:appcompat:1.6.1'; implementation 'com.google.android.material:material:1.9.0' }")
          create_file("app/src/main/AndroidManifest.xml", '<?xml version="1.0" encoding="utf-8"?><manifest xmlns:android="http://schemas.android.com/apk/res/android"><application android:label="Genesis 6.0" android:theme="@style/Theme.Material3.DayNight.NoActionBar"><activity android:name=".MainActivity" android:exported="true" android:screenOrientation="landscape"><intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter></activity></application></manifest>')
          EOF

          # --- SCRIPT 2: DUAL UI (Overworld + Hidden Battle Screen) ---
          cat << 'EOF' > scripts/2-ui.py
          import os
          def create_file(path, content):
              dir_name = os.path.dirname(path)
              if dir_name: os.makedirs(dir_name, exist_ok=True)
              with open(path, 'w', encoding='utf-8') as f: f.write(content)

          layout = """<?xml version="1.0" encoding="utf-8"?>
          <FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="match_parent" android:background="#000000">
              
              <RelativeLayout android:id="@+id/layer_overworld" android:layout_width="match_parent" android:layout_height="match_parent">
                  <com.genesis.pokemon.GameView android:id="@+id/game_viewport" android:layout_width="match_parent" android:layout_height="match_parent" />
                  <View android:id="@+id/joystick_base" android:layout_width="150dp" android:layout_height="150dp" android:layout_alignParentBottom="true" android:layout_margin="30dp" android:background="@android:drawable/btn_default_small" android:alpha="0.4"/>
                  <RelativeLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_alignParentBottom="true" android:layout_alignParentEnd="true" android:layout_margin="40dp">
                      <Button android:id="@+id/btn_b" android:layout_width="80dp" android:layout_height="80dp" android:text="B" android:backgroundTint="#F44336" android:layout_marginEnd="90dp"/>
                      <Button android:id="@+id/btn_a" android:layout_width="80dp" android:layout_height="80dp" android:text="A" android:backgroundTint="#2196F3" android:layout_toEndOf="@id/btn_b" android:layout_marginTop="-30dp"/>
                  </RelativeLayout>
              </RelativeLayout>

              <RelativeLayout android:id="@+id/layer_battle" android:layout_width="match_parent" android:layout_height="match_parent" android:background="#FFFFFF" android:visibility="gone">
                  <TextView android:id="@+id/battle_text" android:layout_width="match_parent" android:layout_height="100dp" android:layout_alignParentBottom="true" android:background="#EEEEEE" android:padding="16dp" android:textColor="#000000" android:textSize="18sp" android:text="A wild Pokemon appeared!"/>
                  <LinearLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_above="@id/battle_text" android:layout_alignParentEnd="true" android:orientation="vertical" android:background="#DDDDDD">
                      <Button android:id="@+id/btn_fight" android:layout_width="120dp" android:layout_height="wrap_content" android:text="FIGHT"/>
                      <Button android:id="@+id/btn_bag" android:layout_width="120dp" android:layout_height="wrap_content" android:text="BAG (CATCH)"/>
                      <Button android:id="@+id/btn_run" android:layout_width="120dp" android:layout_height="wrap_content" android:text="RUN"/>
                  </LinearLayout>
              </RelativeLayout>

          </FrameLayout>"""
          create_file("app/src/main/res/layout/activity_main.xml", layout)
          EOF

          # --- SCRIPT 3: ROUTE ASSETS ---
          cat << 'EOF' > scripts/3-assets.py
          import os, requests
          os.makedirs("app/src/main/assets/sprites", exist_ok=True)
          
          # Trainer
          with open("app/src/main/assets/sprites/trainer.png", 'wb') as f: 
              f.write(requests.get("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/trainers/1.png").content)
          
          # Route 101 Encounters
          for p in ["bulbasaur", "pikachu", "zigzagoon", "wurmple", "rattata"]:
              r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{p}").json()
              with open(f"app/src/main/assets/sprites/{p}.png", 'wb') as f: 
                  f.write(requests.get(r['sprites']['front_default']).content)
          EOF

          # --- SCRIPT 4: THE ENGINE (Encounter Triggers) ---
          cat << 'EOF' > scripts/4-engine.py
          import os
          def create_file(path, content):
              dir_name = os.path.dirname(path)
              if dir_name: os.makedirs(dir_name, exist_ok=True)
              with open(path, 'w', encoding='utf-8') as f: f.write(content)

          java_path = "app/src/main/java/com/genesis/pokemon"

          create_file(f"{java_path}/SpriteManager.java", "package com.genesis.pokemon; import android.content.Context; import android.graphics.Bitmap; import android.graphics.BitmapFactory; import java.util.HashMap; public class SpriteManager { private static HashMap<String, Bitmap> cache = new HashMap<>(); public static Bitmap get(Context ctx, String name) { if (cache.containsKey(name)) return cache.get(name); try { Bitmap b = BitmapFactory.decodeStream(ctx.getAssets().open(\"sprites/\" + name + \".png\")); cache.put(name, b); return b; } catch (Exception e) { return null; } } }")

          create_file(f"{java_path}/GameView.java", """package com.genesis.pokemon;
          import android.content.Context;
          import android.graphics.*;
          import android.util.AttributeSet;
          import android.view.SurfaceView;

          public class GameView extends SurfaceView implements Runnable {
              private Thread thread;
              public boolean r;
              public float px=128, py=128;
              public float vx=0, vy=0;
              public boolean isBattling = false;
              public MainActivity activity; // Reference to trigger UI
              
              // 0=Path, 1=Wall, 2=Tall Grass (Encounter Zone)
              private int[][] map = {
                  {1,1,1,1,1,1,1,1,1,1},
                  {1,0,0,0,2,2,2,0,0,1},
                  {1,0,1,0,2,2,2,0,0,1},
                  {1,0,0,0,0,0,0,0,0,1},
                  {1,1,1,1,1,1,1,1,1,1}
              };

              public GameView(Context c, AttributeSet a) { super(c, a); }

              @Override public void run() {
                  while (r) {
                      if (!getHolder().getSurface().isValid()) continue;
                      Canvas c = getHolder().lockCanvas();
                      if (!isBattling) update();
                      drawGame(c);
                      getHolder().unlockCanvasAndPost(c);
                      try { Thread.sleep(16); } catch (Exception e) {}
                  }
              }

              private void update() {
                  float s = 6; 
                  float tx = px + (vx * s), ty = py + (vy * s);

                  int gridX = (int)(tx / 64), gridY = (int)(ty / 64);
                  if (gridY >= 0 && gridY < map.length && gridX >= 0 && gridX < map[0].length) {
                      if (map[gridY][gridX] != 1) { // If not wall
                          px = tx; py = ty;
                          
                          // ENCOUNTER LOGIC
                          if (map[gridY][gridX] == 2 && (vx != 0 || vy != 0)) {
                              if (Math.random() < 0.02) { // 2% chance per frame in grass
                                  isBattling = true;
                                  vx = 0; vy = 0; // Stop moving
                                  if (activity != null) activity.startBattle("zigzagoon");
                              }
                          }
                      }
                  }
              }

              private void drawGame(Canvas c) {
                  c.drawColor(Color.BLACK);
                  Paint p = new Paint();
                  for (int y=0; y<map.length; y++) {
                      for (int x=0; x<map[0].length; x++) {
                          if (map[y][x] == 1) p.setColor(Color.parseColor("#2E7D32")); // Tree
                          else if (map[y][x] == 2) p.setColor(Color.parseColor("#81C784")); // Tall Grass
                          else p.setColor(Color.parseColor("#AED581")); // Path
                          c.drawRect(x*64, y*64, (x+1)*64, (y+1)*64, p);
                      }
                  }
                  Bitmap trainer = SpriteManager.get(getContext(), "trainer");
                  if (trainer != null) c.drawBitmap(trainer, px-32, py-32, null);
              }
              public void resume() { r = true; thread = new Thread(this); thread.start(); }
              public void pause() { r = false; }
          }""")
          EOF

          # --- SCRIPT 5: RPG BATTLE SYSTEM ---
          cat << 'EOF' > scripts/5-battle.py
          import os
          def create_file(path, content):
              dir_name = os.path.dirname(path)
              if dir_name: os.makedirs(dir_name, exist_ok=True)
              with open(path, 'w', encoding='utf-8') as f: f.write(content)

          java_path = "app/src/main/java/com/genesis/pokemon"
          
          create_file(f"{java_path}/MainActivity.java", """package com.genesis.pokemon;
          import android.app.Activity;
          import android.os.Bundle;
          import android.view.MotionEvent;
          import android.view.View;
          import android.widget.TextView;

          public class MainActivity extends Activity {
              private GameView gv;
              private View layerOverworld, layerBattle;
              private TextView battleText;
              
              // Battle State
              private String currentWildPokemon;
              private int wildHP = 100, wildMaxHP = 100;

              @Override protected void onCreate(Bundle b) {
                  super.onCreate(b);
                  setContentView(R.layout.activity_main);
                  
                  gv = findViewById(R.id.game_viewport);
                  gv.activity = this; // Link engine to UI
                  
                  layerOverworld = findViewById(R.id.layer_overworld);
                  layerBattle = findViewById(R.id.layer_battle);
                  battleText = findViewById(R.id.battle_text);
                  
                  // Joystick Logic
                  findViewById(R.id.joystick_base).setOnTouchListener((v, e) -> {
                      if (e.getAction() == MotionEvent.ACTION_UP) { gv.vx = 0; gv.vy = 0; } 
                      else {
                          float dx = e.getX() - (v.getWidth()/2f), dy = e.getY() - (v.getHeight()/2f);
                          float mag = (float)Math.sqrt(dx*dx + dy*dy);
                          if (mag > 0) { gv.vx = dx/mag; gv.vy = dy/mag; }
                      }
                      return true;
                  });

                  // Battle Menu Logic
                  findViewById(R.id.btn_run).setOnClickListener(v -> endBattle("Got away safely!"));
                  
                  findViewById(R.id.btn_fight).setOnClickListener(v -> {
                      wildHP -= 25; // Simple tackle
                      if (wildHP <= 0) endBattle("Wild " + currentWildPokemon + " fainted!");
                      else battleText.setText("You attacked! Wild " + currentWildPokemon + " HP: " + wildHP);
                  });

                  // CATCHING MECHANIC
                  findViewById(R.id.btn_bag).setOnClickListener(v -> {
                      battleText.setText("You threw a Poké Ball!");
                      // Standard Gen 3/4 Math: ((3*MaxHP - 2*CurrHP) / (3*MaxHP)) * CatchRate
                      float catchRate = 0.5f; // 50% base for standard ball
                      float catchChance = (((3f * wildMaxHP) - (2f * wildHP)) / (3f * wildMaxHP)) * catchRate;
                      
                      if (Math.random() < catchChance) {
                          endBattle("Gotcha! " + currentWildPokemon + " was caught!");
                      } else {
                          battleText.setText("Oh no! The Pokémon broke free!");
                      }
                  });
              }

              // State Machine Transitions
              public void startBattle(final String pokemonName) {
                  runOnUiThread(() -> {
                      currentWildPokemon = pokemonName;
                      wildHP = 100; wildMaxHP = 100;
                      layerOverworld.setVisibility(View.GONE);
                      layerBattle.setVisibility(View.VISIBLE);
                      battleText.setText("A wild " + pokemonName + " appeared!");
                  });
              }

              public void endBattle(final String message) {
                  runOnUiThread(() -> {
                      battleText.setText(message);
                      // Wait 1.5 seconds so player can read message, then return to world
                      layerBattle.postDelayed(() -> {
                          layerBattle.setVisibility(View.GONE);
                          layerOverworld.setVisibility(View.VISIBLE);
                          gv.isBattling = false; // Resume engine
                      }, 1500);
                  });
              }

              @Override protected void onResume() { super.onResume(); gv.resume(); }
              @Override protected void onPause() { super.onPause(); gv.pause(); }
          }""")
          EOF

      - name: Execute Genesis Pipeline
        run: |
          cd MyPokemonGame
          python scripts/1-scaffold.py
          python scripts/2-ui.py
          python scripts/3-assets.py
          python scripts/4-engine.py
          python scripts/5-battle.py

      - name: Build APK (Pinned Gradle 8.7)
        run: |
          cd MyPokemonGame
          gradle wrapper --gradle-version 8.7
          chmod +x gradlew
          ./gradlew assembleDebug

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: Genesis-6.0-APK
          path: MyPokemonGame/app/build/outputs/apk/debug/app-debug.apk

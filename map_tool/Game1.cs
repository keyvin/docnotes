using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using MonoGame.Extended;
using MonoGame.Extended.Shapes;
using System;
using System.Collections;
using System.Collections.Generic;

namespace map_tool
{
    public enum tool_selection { wall, door, locked_door, one_way, invisible, impassible}; 
    
    public class Pallette
    {
        public Dictionary<tool_selection, Texture2D> selections;
        public tool_selection curr_tool;
        public Vector2 screenLocation;
        public Vector2 extents;
        public Pallette(Vector2 sLoc, Vector2 ext)
        {
            selections = new Dictionary<tool_selection, Texture2D>();
            screenLocation = sLoc;
            extents = ext;

        }
        public void LoadToolImages(ContentManager Content)
        {
            selections.Add(tool_selection.wall, Content.Load<Texture2D>("assets/hor"));
            selections.Add(tool_selection.door, Content.Load<Texture2D>("assets/hor_door"));

        }
        public void DrawToolbox(GraphicsDevice d, SpriteBatch target)
        {
            if ((d.Viewport.Width > 200) && (d.Viewport.Height > 200))
            {
                target.Begin();
                MonoGame.Extended.ShapeExtensions.DrawRectangle(target, new RectangleF(screenLocation.X, screenLocation.Y, extents.X, extents.Y), Color.White, 2);
                target.Draw(selections[tool_selection.wall], new Vector2(screenLocation.X + 10, screenLocation.Y + 10), Color.White);
                target.Draw(selections[tool_selection.door], new Vector2(screenLocation.X+70, screenLocation.Y + 10), Color.White);
                target.End();
            }
            return;
        }
        public bool HandleClick(MouseState e)
        {
            if (e.X > screenLocation.X && e.X < screenLocation.X +extents.X) 
                if (e.Y > screenLocation.Y && e.Y < screenLocation.Y + extents.Y)
                {
                    
                    return true;
                }
            
            return false;
        }

    }
    
    public class Game1 : Game
    {
        private GraphicsDeviceManager _graphics;
        private SpriteBatch _spriteBatch;
        public bool mouseDown { get; set; }
        public MouseState mouseOld;
        Texture2D hor_wall;
        public List<CircleF> circles;
        Pallette p;
        public Game1()
        {
            
            circles = new List<CircleF>();
            _graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";
        
            IsMouseVisible = true;
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here

            base.Initialize();
        }

        protected override void LoadContent()
        {
            
            _spriteBatch = new SpriteBatch(GraphicsDevice);
            hor_wall = Content.Load<Texture2D>("assets/hor");
            // TODO: use this.Content to load your game content here
            VertexPositionColor[] _vertexPositionColors = new[]
            {
            new VertexPositionColor(new Vector3(0, 0, 1), Color.White),
            new VertexPositionColor(new Vector3(10, 0, 1), Color.White),
            new VertexPositionColor(new Vector3(10, 10, 1), Color.White),
            new VertexPositionColor(new Vector3(0, 10, 1), Color.White)
            };
             BasicEffect _basicEffect = new BasicEffect(GraphicsDevice);
            _basicEffect.World = Matrix.CreateOrthographicOffCenter(
                0, GraphicsDevice.Viewport.Width, GraphicsDevice.Viewport.Height, 0, 0, 1);
            p = new Pallette(new Vector2(GraphicsDevice.Viewport.Width-140,10), new Vector2(120,200));
            p.LoadToolImages(Content);
        }

        protected override void Update(GameTime gameTime)
        {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // TODO: Add your update logic here
            MouseState mouseState = Mouse.GetState();
            if (mouseState.LeftButton == ButtonState.Pressed && mouseOld.LeftButton == ButtonState.Released)
            {
                mouseOld = mouseState;
                // do something here
            }
            if (mouseState.LeftButton == ButtonState.Released && mouseOld.LeftButton == ButtonState.Pressed)
            { 

                if (Math.Abs(mouseOld.X - mouseState.X) < 5 && Math.Abs(mouseOld.Y - mouseState.Y) < 5)
                {
                    if (!p.HandleClick(mouseState))
                        circles.Add(new CircleF(new Point2(mouseState.X, mouseState.Y), 30));
                    
                }
                mouseOld = mouseState;
            }
            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);
            _spriteBatch.Begin();
            _spriteBatch.Draw(hor_wall, new Vector2(0, 0), Color.White);
            foreach (var c in circles)
            {
                MonoGame.Extended.ShapeExtensions.DrawCircle(_spriteBatch, c, 20, Color.White, 2);
            }
                MonoGame.Extended.ShapeExtensions.DrawRectangle(_spriteBatch, new RectangleF(80, 80, 200, 200), Color.White, 2);
            _spriteBatch.End();
            p.DrawToolbox(GraphicsDevice, _spriteBatch);
            // TODO: Add your drawing code here

            base.Draw(gameTime);
        }
    }
}

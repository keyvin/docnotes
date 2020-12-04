using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Microsoft.Xna.Framework.Input.Touch;
using MonoGame.Extended;
using MonoGame.Extended.Screens;
using MonoGame.Extended.Shapes;
using System;
using System.Collections;
using System.Collections.Generic;
//using System.Reflection.Metadata.Ecma335;

namespace android
{
    public enum tool_selection { wall, door, locked_door, one_way, invisible, impassible };
    public class tool_item
    {
        public tool_selection type { get; set; }
        public Texture2D image { get; set; }
        public Vector2 location { get; set; }
        public Vector2 extent { get; set; }
        public float scale { get; set; }
        public bool selected { get; set; }

    }

    public class Pallette
    {
        public Dictionary<tool_selection, Texture2D> selections;
        public List<tool_selection> order;
        public List<tool_item> tool_items;
        public tool_selection curr_tool;
        public Vector2 screenLocation;
        public Vector2 extents;
        public float horizontalSpacingPct { get; set; }
        public int verticalSpacingPct;
        public string[] orderedAssets;
        public Pallette(Vector2 sLoc, Vector2 ext)
        {
            selections = new Dictionary<tool_selection, Texture2D>();
            tool_items = new List<tool_item>();
            orderedAssets = new string[] { "assets/hor", "assets/hor_door", "assets/hor_door" };
            horizontalSpacingPct = .3f;
            order = new List<tool_selection>();
            order.Add(tool_selection.wall);
            order.Add(tool_selection.door);
            order.Add(tool_selection.impassible);
            screenLocation = sLoc;
            extents = ext;

        }
        public void LoadToolImages(Microsoft.Xna.Framework.Content.ContentManager Content)
        {
            for (int itemNum = 0; itemNum < order.Count; itemNum++)
            {
                tool_item working = new tool_item();
                working.type = order[itemNum];
                working.image = Content.Load<Texture2D>(orderedAssets[itemNum]);
                working.location = calcXY(itemNum);
                //aspect determined by horizontal size (will be square)
                working.extent = new Vector2(extents.X * horizontalSpacingPct, extents.X * horizontalSpacingPct);
                working.selected = false;
                working.scale = working.extent.X / working.image.Width;
                tool_items.Add(working);
            }

        }
        public void DrawToolbox(GraphicsDevice d, SpriteBatch target)
        {
            if ((d.Viewport.Width > 200) && (d.Viewport.Height > 200))
            {
                target.Begin();
                MonoGame.Extended.ShapeExtensions.DrawRectangle(target, new RectangleF(screenLocation.X, screenLocation.Y, extents.X, extents.Y), Color.White, 4);
                foreach (var tool in tool_items)
                {
                    target.Draw(tool.image, tool.location, null, Color.White,
                                0f,
                                Vector2.Zero, tool.scale, SpriteEffects.None, 0f);

                    if (tool.selected == true)
                    {
                        MonoGame.Extended.ShapeExtensions.DrawRectangle(target, new RectangleF(tool.location.X - 3, tool.location.Y - 3, tool.extent.X + 3, tool.extent.X + 3), Color.Black, 3);
                    }

                }
            }
            target.End();

            return;
        }
        private Vector2 calcXY(int num)
        {
            Vector2 working = new Vector2(0, 0);
            int column = num % 2;
            working.X = (.10f * extents.X) + (column * (extents.X * .45f)) + screenLocation.X;
            working.Y = ((.10f * extents.Y) + (extents.X * horizontalSpacingPct)) * Convert.ToInt32(num / 2) + screenLocation.Y;

            return working;
        }
        public bool HandleClick(Vector2 e)
        {
            if (e.X > screenLocation.X && e.X < screenLocation.X + extents.X)
                if (e.Y > screenLocation.Y && e.Y < screenLocation.Y + extents.Y)
                {

                    for (int j = 0; j < tool_items.Count; j++)
                    {
                        if (e.X > tool_items[j].location.X && e.X < tool_items[j].location.X + tool_items[j].extent.X)
                            if (e.Y > tool_items[j].location.Y && e.Y < tool_items[j].location.Y + tool_items[j].extent.Y)
                            {


                                tool_items[j].selected = !tool_items[j].selected;
                                return true;
                            }

                    }

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
            p = new Pallette(new Vector2(GraphicsDevice.Viewport.Width - 140, 10), new Vector2(120, 200));
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
                    if (!p.HandleClick(new Vector2(mouseState.X, mouseState.Y)))
                        circles.Add(new CircleF(new Point2(mouseState.X, mouseState.Y), 30));

                }
                mouseOld = mouseState;
            }
            TouchCollection tc = TouchPanel.GetState();
            
            
            foreach (TouchLocation tl in tc)
            {
                if (tl.State == TouchLocationState.Released)
                {
                    if (!p.HandleClick(new Vector2(tl.Position.X, tl.Position.Y)))
                        circles.Add(new CircleF(new Point2(tl.Position.X, tl.Position.Y), 30));
                }

                
                   

                // Do something here
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

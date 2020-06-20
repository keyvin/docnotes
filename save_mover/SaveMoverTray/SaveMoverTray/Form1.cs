using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Windows.Forms;

namespace SaveMoverTray
{
    public partial class Form1 : Form
    {
        GameList glist;
        public Form1(GameList a)
        {
            InitializeComponent();
            glist = a;
            this.Resize += new System.EventHandler(this.Form1_Resize);
            glist.LoadList();
            foreach (var name in glist.GetGames())
            {
                List.Items.Add(name);
            }

            
        }
            
        
        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void Form1_Resize(object sender, EventArgs e)
        {
            //if the form is minimized  
            //hide it from the task bar  
            //and show the system tray icon (represented by the NotifyIcon control)  
            if (this.WindowState == FormWindowState.Minimized)
            {
                Hide();
                notifyIcon1.Visible = true;
            }
        }
        private void Form1_Close(object sender, EventArgs e)
        {
            notifyIcon1.Visible = false;
            notifyIcon1.Icon.Dispose();

            notifyIcon1.Dispose();
        }
        private void notifyIcon1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            Show();
            this.WindowState = FormWindowState.Normal;
            notifyIcon1.Visible = false;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            string result;
            result = glist.DoAutoCopy();
            LoggedOutput.Text = LoggedOutput.Text + result;
        }

        private void moveCurrentButton_Click(object sender, EventArgs e)
        {

        }

        private void addButton_Click(object sender, EventArgs e)
        {
            var a = new AddGame();
            
            a.ShowDialog();
            Game gameToAdd = new Game(a.GameName, a.Path, a.AutoCopy);
            if (a.DialogResult == DialogResult.OK)
            {

                gameToAdd.OverWrite = a.OverWrite;
                gameToAdd.AutoCopy = a.AutoCopy;
                if (glist.NameExists(gameToAdd.Name))
                {
                    MessageBox.Show("Error", "Name Exists!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                if (glist.PathExists(gameToAdd.GameDir))
                {
                    MessageBox.Show("Error", "Path belongs to other game!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                glist.AddGame(gameToAdd);

                List.Items.Add(gameToAdd.Name);
            }
        }

        private void fileToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void saveListToolStripMenuItem_Click(object sender, EventArgs e)
        {
       
            SaveFileDialog saveFileDialog1 = new SaveFileDialog();

            saveFileDialog1.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*";
            saveFileDialog1.FilterIndex = 1;
            saveFileDialog1.RestoreDirectory = true;

            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                if (saveFileDialog1.FileName != null)
                {
                    // Code to write the stream goes here.
                    glist.SaveList(saveFileDialog1.FileName);
                }
            }
        }
       
        private void restoreListToolStripMenuItem_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.InitialDirectory = "";
                openFileDialog.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*";
                openFileDialog.FilterIndex = 2;
                openFileDialog.RestoreDirectory = true;

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    //Get the path of specified file
                    string filePath = openFileDialog.FileName;

                    //Read the contents of the file into a stream
                    glist.LoadList(filePath);
                    List.Items.Clear();
                    foreach (var name in glist.GetGames())
                    {
                        List.Items.Add(name);
                    }

                }
            }
        }
    }
}

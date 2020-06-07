using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.WindowsAPICodePack.Dialogs;

namespace SaveMoverTray
{
    public partial class AddGame : Form
    {
        public bool Valid { get; set; }
        public bool OverWrite { get; set; }
        public bool AutoCopy { get; set; }
        public string Path{ get; set; }
        public string GameName { get; set; }

        

        public AddGame()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void selectFolder_Click(object sender, EventArgs e)
        {
            var dialog = new CommonOpenFileDialog();
            dialog.IsFolderPicker = true;
            CommonFileDialogResult result = dialog.ShowDialog();
            if (result == CommonFileDialogResult.Ok)
            {
                var filePath = dialog.FileName;
                pathText.Text = filePath;
                Refresh();
            }
        }

        private void selectFileButton_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.InitialDirectory = "c:\\";
                //openFileDialog.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
                //openFileDialog.FilterIndex = 2;
                openFileDialog.RestoreDirectory = true;

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {

                    var filePath = openFileDialog.FileName;
                    pathText.Text = filePath;
                    //Refresh();
                    //Read the contents of the file into a stream
                    /*var fileStream = openFileDialog.OpenFile();

                    using (StreamReader reader = new StreamReader(fileStream))
                    {
                        fileContent = reader.ReadToEnd();
                    }*/
                }
            }
        }

        private void OkButton_Click(object sender, EventArgs e)
        {
            GameName = gameName.Text;
            Path = pathText.Text;
            AutoCopy = autoBox.Checked;
            OverWrite = overwriteBox.Checked;
            if (!System.IO.Directory.Exists(Path) && !System.IO.File.Exists(Path))
            {
                MessageBox.Show("Error", "Path doesn't exist!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else if (GameName == "")
            {
                MessageBox.Show("Error", "Must provide name!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                
                DialogResult = DialogResult.OK; 
                Valid = true;
                Hide();
            }
            
        }

        private void CancelButton_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
            Hide();
        }
    }
}

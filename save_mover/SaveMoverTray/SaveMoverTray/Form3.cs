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
    public partial class Form3 : Form
    {
        public string savePath;
        public bool valid;
        public Form3(string path)
        {
            
            InitializeComponent();
            filePathText.Text = path;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string path = filePathText.Text;
            if (!System.IO.Directory.Exists(path) && !System.IO.File.Exists(path))
            {
                MessageBox.Show("Error", "Path doesn't exist!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {

                DialogResult = DialogResult.OK;
                valid = true;
                savePath = filePathText.Text;
                Hide();
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            var dialog = new CommonOpenFileDialog();
            dialog.IsFolderPicker = true;
            CommonFileDialogResult result = dialog.ShowDialog();
            if (result == CommonFileDialogResult.Ok)
            {
                var filePath = dialog.FileName;
                filePathText.Text = filePath;
                Refresh();
            }
        }

        private void button2_Click(object sender, EventArgs e)            
        {
            DialogResult = DialogResult.Cancel;
            Hide();
        }
    }
}

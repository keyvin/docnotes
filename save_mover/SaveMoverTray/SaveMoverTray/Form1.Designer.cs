namespace SaveMoverTray
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            notifyIcon1.Visible = true;
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
            
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.LoggedOutput = new System.Windows.Forms.TextBox();
            this.moveCurrentButton = new System.Windows.Forms.Button();
            this.moveAllButton = new System.Windows.Forms.Button();
            this.addButton = new System.Windows.Forms.Button();
            this.deleteButton = new System.Windows.Forms.Button();
            this.List = new System.Windows.Forms.ListBox();
            this.SuspendLayout();
            // 
            // notifyIcon1
            // 
            this.notifyIcon1.Icon = ((System.Drawing.Icon)(resources.GetObject("notifyIcon1.Icon")));
            this.notifyIcon1.Text = "notifyIcon1";
            this.notifyIcon1.Visible = true;
            this.notifyIcon1.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.notifyIcon1_MouseDoubleClick);
            // 
            // timer1
            // 
            this.timer1.Enabled = true;
            this.timer1.Interval = 1000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // LoggedOutput
            // 
            this.LoggedOutput.Location = new System.Drawing.Point(12, 113);
            this.LoggedOutput.Multiline = true;
            this.LoggedOutput.Name = "LoggedOutput";
            this.LoggedOutput.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.LoggedOutput.Size = new System.Drawing.Size(327, 128);
            this.LoggedOutput.TabIndex = 0;
            // 
            // moveCurrentButton
            // 
            this.moveCurrentButton.Location = new System.Drawing.Point(12, 247);
            this.moveCurrentButton.Name = "moveCurrentButton";
            this.moveCurrentButton.Size = new System.Drawing.Size(83, 23);
            this.moveCurrentButton.TabIndex = 1;
            this.moveCurrentButton.Text = "Move Current";
            this.moveCurrentButton.UseVisualStyleBackColor = true;
            this.moveCurrentButton.Click += new System.EventHandler(this.moveCurrentButton_Click);
            // 
            // moveAllButton
            // 
            this.moveAllButton.Location = new System.Drawing.Point(101, 247);
            this.moveAllButton.Name = "moveAllButton";
            this.moveAllButton.Size = new System.Drawing.Size(75, 23);
            this.moveAllButton.TabIndex = 2;
            this.moveAllButton.Text = "Move All";
            this.moveAllButton.UseVisualStyleBackColor = true;
            // 
            // addButton
            // 
            this.addButton.Location = new System.Drawing.Point(182, 247);
            this.addButton.Name = "addButton";
            this.addButton.Size = new System.Drawing.Size(75, 23);
            this.addButton.TabIndex = 3;
            this.addButton.Text = "Add";
            this.addButton.UseVisualStyleBackColor = true;
            this.addButton.Click += new System.EventHandler(this.addButton_Click);
            // 
            // deleteButton
            // 
            this.deleteButton.Location = new System.Drawing.Point(264, 246);
            this.deleteButton.Name = "deleteButton";
            this.deleteButton.Size = new System.Drawing.Size(75, 23);
            this.deleteButton.TabIndex = 4;
            this.deleteButton.Text = "Delete";
            this.deleteButton.UseVisualStyleBackColor = true;
            // 
            // List
            // 
            this.List.FormattingEnabled = true;
            this.List.Location = new System.Drawing.Point(12, 12);
            this.List.Name = "List";
            this.List.ScrollAlwaysVisible = true;
            this.List.Size = new System.Drawing.Size(327, 95);
            this.List.TabIndex = 5;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(352, 291);
            this.Controls.Add(this.List);
            this.Controls.Add(this.deleteButton);
            this.Controls.Add(this.addButton);
            this.Controls.Add(this.moveAllButton);
            this.Controls.Add(this.moveCurrentButton);
            this.Controls.Add(this.LoggedOutput);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "Save Mover";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.TextBox LoggedOutput;
        private System.Windows.Forms.Button moveCurrentButton;
        private System.Windows.Forms.Button moveAllButton;
        private System.Windows.Forms.Button addButton;
        private System.Windows.Forms.Button deleteButton;
        private System.Windows.Forms.ListBox List;
    }
}


#include <stdio.h>
#include <stdlib.h>


typedef struct NODE {
  char value;
  struct NODE *l;
  struct NODE *r;
} node;


typedef struct STACK_EL {
  struct NODE *value;
  struct STACK_EL *next;
} stack_el;

stack_el *stack_root = NULL;
node *tree_root = NULL;

int max_depth = 0;
char cdump[10][200];
int dump_counter = 0;

void push(node *value){
  stack_el *working;
  working = (stack_el *) malloc(sizeof(stack_el));
  working->value = value;
  working->next = stack_root;
  stack_root = working;
  return;
}

node * pop(){
  stack_el *working = NULL;
  node *return_val = NULL;
  if (stack_root != NULL){
    working = stack_root;
    stack_root = stack_root->next;
    return_val = working->value;
    free(working);
  }
  else
    return_val = NULL;

  return return_val;
}

node *mk_node(char val){
  node * working = NULL;
  working = (node *) malloc(sizeof(node));
  working->value = val;
  working->l = NULL;
  working->r = NULL;
  return working;
}


void depth(int curr_depth, node *current){
  if (max_depth < curr_depth)
    max_depth = curr_depth;
  if (current->l)
    depth(curr_depth+1, current->l);
  if (current->r)
    depth(curr_depth+1, current->r);
  printf("%c\n", current->value);
  return ;
}


int dump(int curr_depth, int target, node *current){
  if (curr_depth == target){
    if (current->value != '\0')
      cdump[curr_depth][dump_counter++] = current->value;
    else
      cdump[curr_depth][dump_counter++] = 'N';
  }
  if (current->l)
    dump(curr_depth+1, target, current->l);
  if (current->r)
    dump(curr_depth+1, target, current->r);
  return 0 ;
}


void do_dump(){
  int d = 0;
  int a = 0;
  //zero dump
  for (int a = 0; a < 10; a++){
    for (int d = 0; d < 20; d++){
      cdump[a][d] = '\0';
    }
  }
  //results stored in max_depth
  depth(0, tree_root);	
  d = max_depth;
  printf("Max Depth %d\n", d);
  for (int a = 0; a<= max_depth; a++){
    dump_counter = 0;
    dump(0, a, tree_root);
    printf("Level %d:  %s\n", a, cdump[a]);
	  
  }
  return;
}


void parse(char *s )
{
  int position = 0;
  node *working = NULL;
  if (*s == '\0')
    return;
  tree_root = mk_node(s[position]);
  position++;
  

  
  while (s[position] != '\0'){
    //read token (should be operator) and push tree left
    working = tree_root;
    tree_root = mk_node(s[position]);
    tree_root->l = working;
    tree_root->value = s[position];
    position++;
    tree_root->r = mk_node(s[position]);
    position++;    
  }
  return;
}

int main(int argv, char **argc){
  parse("1+2+3+4");
  do_dump(tree_root);
  return 0;
}
  
    
    
  
  



  

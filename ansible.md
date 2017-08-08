Ansible vault
ansible-valut create <file-name>      -  encrpy the file
ansible-valut edit <file-name>      -  edit the file
ansible-valut edit <file-name>      -  edit the file
ansible-vault decrypt foo.yml       - decypt file

ansible-vault encrypt_string "42"   - encryt string

put encoded value to somewhare in playbook like global var ( | for multi lines)
notsecret: myvalue
license: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653236336462626566653063336164663966303231363934653561363964363833313662
          6431626536303530376336343832656537303632313433360a626438346336353331386135323734
          62656361653630373231613662633962316233633936396165386439616533353965373339616234
          3430613539666330390a313736323265656432366236633330313963326365653937323833366536
          34623731376664623134383463316265643436343438623266623965636363326136
other_plain_text: othervalue


Ansible data type

string, int, bool, list, map 

data_test: 
   foo: 5         # this is int 
   goo: hello     # this is string in python like 'hello'


group counting 
 (groups['dcos_slaves'] | length) +  (groups['dcos_slaves_public'] | length)


jinja expression 

{% ... %} for control statements
{{ ... }} for expressions
{# ... #} for comments

Ansible multiline commands
shell: |


Ansible tagging

ansible-playbook site.yml --limit webservers


Filters

To escape special characters within a regex, use the “regex_escape” filter:

# convert '^f.*o(.*)$' to '\^f\.\*o\(\.\*\)\$'
{{ '^f.*o(.*)$' | regex_escape() }}


To replace text in a string with regex, use the “regex_replace” filter:

# convert "ansible" to "able"
{{ 'ansible' | regex_replace('^a.*i(.*)$', 'a\\1') }}

# convert "foobar" to "bar"
{{ 'foobar' | regex_replace('^f.*o(.*)$', '\\1') }}
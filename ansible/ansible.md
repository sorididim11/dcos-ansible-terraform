# Ansible tips

## Ansible vault
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


## Ansible data type
data_test: 
   foo: 5         # this is int 
   foo: 1.0       # float
   goo: hello     # this is string in python like 'hello'

## Group counting 
 (groups['dcos_slaves'] | length) +  (groups['dcos_slaves_public'] | length)

### Group index 
Play을 그룹중에 하나의 서버만 실행할때 배열의 인덱스를 사용할 수있다. 
hosts: dcos_cli[0]  //그룹의 첫번째
webservers[-1]      //그룹의 두번째

### Ansible multiline commands
shell: |
         command1
         command2
         commandN

## Ansible tagging
ansible-playbook site.yml --limit webservers


### jinja expression 
* {% ... %} for control statements 
* {{ ... }} for expressions
* {# ... #} for comments


### Filters
To escape special characters within a regex, use the “regex_escape” filter:

* convert '^f.*o(.*)$' to '\^f\.\*o\(\.\*\)\$'
    {{ '^f.*o(.*)$' | regex_escape() }}

* To replace text in a string with regex, use the “regex_replace” filter:
    convert "ansible" to "able"
    {{ 'ansible' | regex_replace('^a.*i(.*)$', 'a\\1') }}

* convert "foobar" to "bar"
    {{ 'foobar' | regex_replace('^f.*o(.*)$', '\\1') }}


### Block operators

* The > is a folding block operator. That is, it joins multiple lines together by spaces.
key: >
  This text
  has multiple
  lines
Would assign the value This text has multiple lines\n to key

* The | character is a literal block operator. This is probably what you want for multi-line shell scipts

key: |
  This text
  has multiple
  lines
Would assign the value This text\nhas multiple\nlines\n to key

ex) - name: iterate user groups
      shell: |
        ls -l
        systemctl restart ntpd
        cp files /etc

## loop
### show all the hosts matching the pattern, ie all but the group www
- debug:
    msg: "{{ item }}"
  with_inventory_hostnames:
    - all:!www
# ansible-saltstack-dynamic-inventory
Generate a dynamic Ansible inventory of Saltstack minions using the Python salt client API

## Requirements

1. Run from the salt master server.

2. Requires access to the salt Python module. 
   - If your Ansible is housed in a virtualenv source the venv and install salt. Otherwise the venv ansible will call the python script and not be able to find Python salt modules.
   
     ```
     source ../venv/bin/activate
     pip install salt
     ```

## Checking results
- Check the list of minions the script provides

  ```
  ./saltstack_inventory.py --list
  ```

- Check an individual host (only returns ipv4)

  ```
  ./saltstack_inventory.py --list store-0
  ```


## Usage
1. Download the `saltstack_inventory.py` script
2. Execute `ansible` or `ansible-playbook` using `--inventory <path>/saltstack_inventory.py`

   ```
   # ansible --inventory ./saltstack_inventory.py -m ping stor\*

   store-0 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   store-5 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   store-4 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   store-2 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   store-1 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   store-3 | SUCCESS => {
       "changed": false,
       "ping": "pong"
   }
   ```

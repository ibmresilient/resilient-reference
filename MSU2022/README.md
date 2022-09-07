# IBM MasterSkills September '22: IBM **Security** QRadar SOAR Labs

![screenshot](./logo.png)

***Shane Curtin & Bo Bleckel, App Engineers, IBM **Security** QRadar SOAR***

---

## Lab Guides
 1. [Part I: Developing My First App](Lab%20Guides/Part%20I:%20Developing%20My%20First%20App/README.md)
 2. [Part II: Advanced Development of Playbooks](Lab%20Guides/Part%20II:%20Advanced%20Development%20of%20Playbooks/README.md)

---

## Lab Assets

* Click [here](./Lab%20Assets/) to access files needed during the lab

---

## Custom Apps

* Click [here](./Custom%20Apps/) to access some custom app.zips that are used

## Tips
- [Copy/Paste in SkyTap Terminal](#copypaste-in-skytap-terminal)
- [Copy/Paste in SkyTap FireFox Browser](#copypaste-in-skytap-firefox-browser)
- [Restart SOAR Service](#restart-soar-service)
- [View SOAR Logs](#view-soar-logs)
- [AppHost Commands](#apphost-commands)
### Copy/Paste in SkyTap Terminal

* Copy:
  ```
  CTRL + SHIFT + C
  ```

* Paste:
  ```
  CTRL + SHIFT + V
  ```

### Copy/Paste in SkyTap FireFox Browser

* Copy:
  ```
  CTRL + C
  ```

* Paste:
  ```
  CTRL + V
  ```
### Restart SOAR Service
```
$ sudo systemctl restart resilient
```

### View SOAR Logs
```
$ sudo tail -f /usr/share/co3/logs/client.log
```

### AppHost Commands

* Get Deployments:
  ```
  $ sudo kubectl get deployments -L app.kubernetes.io/instance -A
  ```

* Get Logs:
  ```
  $ sudo kubectl logs deployment/<deployment_name> -f -n <namespace>
  ```

---
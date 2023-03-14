// ignore_for_file: prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';

class buttonSetting extends StatelessWidget {
  buttonSetting(
      {Key? key,
      required this.title,
      required this.icon,
      required this.onClicked});

  String title;
  IconData icon;
  VoidCallback onClicked;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onClicked,
      child: Container(
        decoration: const BoxDecoration(
            border: Border(bottom: BorderSide(color: Colors.grey, width: 0.5)),
            //color: Colors.amber
            ),
        margin: const EdgeInsets.symmetric(vertical: 8),
        height: 48,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Icon(icon),
                const SizedBox(
                  width: 16,
                ),
                Text(
                  title,
                  style: const TextStyle(
                      fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ],
            ),
            const Icon(Icons.arrow_forward_ios)
          ],
        ),
      ),
    );
  }
}

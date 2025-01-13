import React from 'react';
import styles from '../styles/InternshipTable.module.css';

export default function InternshipTable({ internships, onDelete }) {
  const getRowClass = (status) => {
    switch (status.toLowerCase()) {
      case 'applied':
        return styles['row-applied'];
      case 'denied':
        return styles['row-denied'];
      case 'oa':
      case 'ti':
        return styles['row-oa-ti'];
      case 'position offered':
        return styles['row-offered'];
      default:
        return '';
    }
  };

    return (
      <div className={styles['table-container']}>
        <table className={styles['styled-table']}>
          <thead>
            <tr>
              <th>Company</th>
              <th>Position</th>
              <th>Status</th>
              <th>Date Applied</th>
            </tr>
          </thead>
          <tbody>
            {internships.map((internship, index) => (
              <tr key={internship.date_applied} className={getRowClass(internship.status)}>
                <td>{internship.company}</td>
                <td>{internship.position}</td>
                <td>{internship.status}</td>
                <td>{internship.date_applied}</td>
                <td>
                  <button className={styles['delete-button']} onClick={() => onDelete(internship._id)}>Remove</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }